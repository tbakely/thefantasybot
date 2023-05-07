import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from lxml import etree
import os


pd.options.display.float_format = "{:.2f}".format


def pull_adp(scoring):

    if scoring == "standard":
        score = "overall"
    elif scoring == "ppr":
        score = "ppr-overall"
    elif scoring == "halfppr":
        score = "half-point-ppr-overall"

    url = f"https://www.fantasypros.com/nfl/adp/{score}.php"
    link = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).content
    soup = bs(link, "html.parser")
    read = etree.HTML(str(soup))

    if scoring == "standard":
        players = read.xpath("//tr/td/a/text()")[:200]
        pos = [n[:2] for n in read.xpath("//tr/td[3]/text()")[:200]]
        adp = read.xpath("//tr/td[9]/text()")[:200]

    elif scoring == "ppr":
        players = read.xpath("//tr/td/a/text()")[:200]
        pos = [n[:2] for n in read.xpath("//tr/td[3]/text()")[:200]]
        adp = read.xpath("//tr/td[10]/text()")[:200]

    elif scoring == "halfppr":
        players = read.xpath("//tr/td/a/text()")[:200]
        pos = [n[:2] for n in read.xpath("//tr/td[3]/text()")[:200]]
        adp = read.xpath("//tr/td[8]/text()")[:200]

    data = {"Player": players, "POS": pos, "ADP": adp}

    df = pd.DataFrame(data)
    df["ADP"] = df["ADP"].astype(float)
    df = df.loc[df["POS"].isin(["QB", "RB", "WR", "TE"])].sort_values("ADP")
    df = df.reset_index(drop=True)

    return df


def pull_projected_points(scoring):

    # we are going to concatenate our individual position dfs into this larger final_df
    final_df = pd.DataFrame()

    # url has positions in lower case
    for position in ["rb", "qb", "te", "wr"]:

        BASE_URL = f"https://www.fantasypros.com/nfl/projections/{position}.php?week=draft&scoring={scoring}&week=draft"

        res = requests.get(BASE_URL)  # format our url with the position
        if res.ok:
            soup = bs(res.content, "html.parser")
            table = soup.find("table", {"id": "data"})
            df = pd.read_html(str(table))[0]

            df.columns = df.columns.droplevel(
                level=0
            )  # our data has a multi-level column index. The first column level is useless so let's drop it.
            df["PLAYER"] = df["Player"].apply(
                lambda x: " ".join(x.split()[:-1])
            )  # fixing player name to not include team
            df["TEAM"] = df["Player"].apply(lambda x: x[-3:].replace(" ", "").strip())

            df["POS"] = position.upper()  # add a position column

            df = df[["PLAYER", "TEAM", "POS", "FPTS"]]
            final_df = pd.concat([final_df, df])  # iteratively add to our final_df
        else:
            print("oops something didn't work right", res.status_code)

    final_df = final_df.sort_values(
        by="FPTS", ascending=False
    )  # sort df in descending order on FPTS column

    return final_df


# choose standard, ppr, or halfppr
def get_draft_board(scoring):

    replacement_players = {"QB": "", "RB": "", "WR": "", "TE": ""}

    adp_df = pull_adp(scoring)

    if scoring == "standard":
        score_system = "STD"
    elif scoring == "ppr":
        score_system = "PPR"
    elif scoring == "halfppr":
        score_system = "HALF"

    projections = pull_projected_points(score_system)
    adp_df_cutoff = adp_df[:90]

    for _, row in adp_df_cutoff.iterrows():
        position = row["POS"]
        player = row["Player"]

        if position in replacement_players:
            replacement_players[position] = player

    replacement_values = {}

    for position, player_name in replacement_players.items():
        player = projections.loc[projections.PLAYER == player_name]
        replacement_values[position] = player["FPTS"].tolist()[0]

    projections = projections.loc[projections.POS.isin(["QB", "RB", "WR", "TE"])]
    projections["VOR"] = projections.apply(
        lambda row: row["FPTS"] - replacement_values.get(row["POS"]), axis=1
    )
    projections["VOR Rank"] = projections["VOR"].rank(ascending=False).astype(int)
    projections = projections.sort_values("VOR", ascending=False)

    adp_df = adp_df.rename({"Player": "PLAYER"}, axis=1)
    complete_df = projections.merge(adp_df, how="left", on=["PLAYER", "POS"])[
        :200
    ].dropna()
    complete_df["ADP Rank"] = complete_df["ADP"].rank().astype(int)
    complete_df["Sleeper Score"] = complete_df["ADP Rank"] - complete_df["VOR Rank"]
    complete_df = complete_df[
        ["PLAYER", "POS", "VOR Rank", "ADP Rank", "Sleeper Score"]
    ]

    return complete_df


# downloads standard, ppr, and halfppr draftboards to a folder
def pull_draft_boards(output_path: str = None):

    score_system_list = ["standard", "ppr", "halfppr"]
    # for score in score_system_list:
    # df = get_draft_board(score)
    # df.to_excel(
    #     f"C:/Users/Tyler/Desktop/NFL Tables/Draft Boards/{score}_asof_{str_date}.xlsx",
    #     index=False,
    # )

    # with pd.ExcelWriter("draftboards.xlsx", engine="openpyxl") as writer:
    #     for score in score_system_list:
    #         df = get_draft_board(score)
    #         df.to_excel(writer, sheet_name=score, index=False)

    df = get_draft_board(score_system_list[0])
    df.index += 1
    df.to_json(
        os.path.join(output_path, f"draftboard_{score_system_list[0]}.json"),
        orient="records",
    )


if __name__ == "__main__":
    pull_draft_boards(
        "/Users/tylerbakely/Desktop/repos/thefantasybot/root/backend/app/data/"
    )

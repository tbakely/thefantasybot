import pandas as pd
import requests
import re
import numpy as np
from sklearn.mixture import GaussianMixture
from bs4 import BeautifulSoup as bs
import os

import warnings

warnings.filterwarnings("ignore")


pd.options.display.float_format = "{:.2f}".format


def apply_regex(regex, string):
    match = re.search(regex, string)
    if match:
        return match.group()
    else:
        return np.nan


def scrape_to_df(url: str, multilevel=False):
    res = requests.get(url)
    if res.ok:
        soup = bs(res.content, "html.parser")
        table = soup.find("table", {"id": "data"})
        df = pd.read_html(str(table))[0]
    else:
        print("oops something didn't work right", res.status_code)
    if multilevel:
        df.columns = df.columns.droplevel(level=0)
    return df


def pull_adp(scoring: str = "STD"):
    scoring_map = {
        "STD": "overall",
        "PPR": "ppr-overall",
        "HALF": "half-point-ppr-overall",
    }

    df = scrape_to_df(f"https://www.fantasypros.com/nfl/adp/{scoring_map[scoring]}.php")
    df["Player"] = df["Player Team (Bye)"].apply(
        lambda x: apply_regex(r"^([a-zA-Z'-.]+\s[a-zA-Z'-]+)(\s(IV|I{2,3}))?", x)
    )
    df["Team"] = df["Player Team (Bye)"].apply(
        lambda x: apply_regex(r"(?!IV|I{1,3})([A-Z]{2,3})", x)
    )
    df["Bye"] = df["Player Team (Bye)"].apply(lambda x: apply_regex(r"\d+", x))
    df["Position"] = df["POS"].apply(lambda x: apply_regex(r"\D+", x))
    df.rename(columns={"AVG": "ADP"}, inplace=True)

    df = df[["Rank", "Player", "Team", "Bye", "Position", "ADP"]]
    return df


def projected_points(scoring: str = "STD", week: str = "draft"):
    """Scrapes projected points from fantasypros.com

    Args:
        scoring (str, optional): 'STD', 'PPR', or 'HALF'. Defaults to 'STD'.
        week (str, optional): _description_. Defaults to 'draft'.

    Returns:
        pd.DataFrame: Finalized dataframe with projected points for the week.
    """
    data = []
    for position in ["qb", "wr", "rb", "te"]:
        df = scrape_to_df(
            f"https://www.fantasypros.com/nfl/projections/{position}.php?week={week}&scoring={scoring}",
            multilevel=True,
        )
        df["Team"] = df["Player"].apply(
            lambda x: apply_regex(r"(?!IV|I{1,3})([A-Z]{2,3})", x)
        )
        df["Player"] = df["Player"].apply(
            lambda x: apply_regex(r"^([a-zA-Z'-.]+\s[a-zA-Z'-]+)(\s(IV|I{2,3}))?", x)
        )
        df["Position"] = position.upper()
        df = df[["Player", "Position", "Team", "FPTS"]]
        data.append(df)
    data = pd.concat(data)

    data = data.sort_values("FPTS", ascending=False).reset_index(drop=True)

    return data


def tiering_players_all(scoring: str = "STD"):
    def tiering_players_pos(scoring: str = "STD", pos: str = "RB"):
        tier_num_mapping = {
            "QB": 8,
            "RB": 11,
            "WR": 12,
            "TE": 9,
        }

        proj_points = projected_points(scoring)
        training = proj_points.loc[proj_points["Position"] == pos]

        gm = GaussianMixture(n_components=tier_num_mapping[pos], random_state=0)
        training["gmm_labels"] = gm.fit_predict(training[["FPTS"]])

        tier_map = {}

        testlist = training["gmm_labels"].tolist()
        count = 1
        for num in testlist:
            if num not in tier_map:
                tier_map[num] = count
                count += 1

        training["Tier"] = training["gmm_labels"].map(tier_map)
        training.drop("gmm_labels", axis=1, inplace=True)
        training.reset_index(drop=True, inplace=True)

        return training

    df_list = []
    for position in ["QB", "RB", "WR", "TE"]:
        temp = tiering_players_pos(scoring=scoring, pos=position)
        df_list.append(temp)

    df = pd.concat(df_list)
    df.reset_index(drop=True, inplace=True)
    df = df[["Player", "Tier"]]

    return df


# choose standard, ppr, or halfppr
def get_draft_board(scoring: str = "STD"):
    replacement_players = {"QB": "", "RB": "", "WR": "", "TE": ""}

    adp_df = pull_adp(scoring)

    projections = projected_points(scoring)

    cutoff = 95
    adp_df_cutoff = adp_df[:cutoff]

    for _, row in adp_df_cutoff.iterrows():
        position = row["Position"]
        player = row["Player"]

        if position in replacement_players:
            replacement_players[position] = player

    replacement_values = {}

    for position, player_name in replacement_players.items():
        player = projections.loc[projections.Player == player_name]
        replacement_values[position] = player["FPTS"].tolist()[0]

    projections = projections.loc[projections.Position.isin(["QB", "RB", "WR", "TE"])]
    projections["VOR"] = projections.apply(
        lambda row: row["FPTS"] - replacement_values.get(row["Position"]), axis=1
    )
    projections["VOR Rank"] = projections["VOR"].rank(ascending=False).astype(int)
    projections = projections.sort_values("VOR", ascending=False)

    complete_df = projections.merge(adp_df, how="left", on=["Player", "Position"])[
        :200
    ].dropna()
    complete_df["ADP Rank"] = complete_df["ADP"].rank().astype(int)
    complete_df["Sleeper Score"] = complete_df["ADP Rank"] - complete_df["VOR Rank"]
    complete_df = complete_df[
        ["Player", "Position", "VOR Rank", "ADP Rank", "Sleeper Score"]
    ]

    player_tiers = tiering_players_all(scoring)

    complete_df = pd.merge(complete_df, player_tiers, how="left", on="Player")

    return complete_df


# downloads standard, ppr, and halfppr draftboards to a folder
def pull_draft_boards(output_path: str = None):
    score_system_list = ["STD", "PPR", "HALF"]
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

    for score_system in score_system_list:
        df = get_draft_board(score_system)
        df.index += 1
        df.to_json(
            os.path.join(output_path, f"draftboard_{score_system}.json"),
            orient="records",
        )


if __name__ == "__main__":
    pull_draft_boards(
        "/Users/tylerbakely/Desktop/repos/thefantasybot/root/backend/app/data/"
    )

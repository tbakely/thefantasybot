import pandas as pd
from sklearn.mixture import GaussianMixture
import os
from datetime import date
from fantasyprosdata import FantasyProsData
import warnings

warnings.filterwarnings("ignore")


class DraftBoard:
    def __init__(self, scoring: str):
        self.scoring = scoring
        self.projections = FantasyProsData(scoring).projected_points()
        self.adp = FantasyProsData(scoring).pull_adp()

    def tiering_players_all(self):
        def tiering_players_pos(pos: str):
            tier_num_mapping = {
                "QB": 8,
                "RB": 11,
                "WR": 12,
                "TE": 9,
            }

            training = self.projections.loc[self.projections["Position"] == pos]

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
            temp = tiering_players_pos(pos=position)
            df_list.append(temp)

        df = pd.concat(df_list)
        df.reset_index(drop=True, inplace=True)
        df = df[["Player", "Tier"]]

        return df

    # choose standard, ppr, or halfppr
    def get_draft_board(self):
        replacement_players = {"QB": "", "RB": "", "WR": "", "TE": ""}

        cutoff = 95
        adp_df_cutoff = self.adp[:cutoff]

        for _, row in adp_df_cutoff.iterrows():
            position = row["Position"]
            player = row["Player"]

            if position in replacement_players:
                replacement_players[position] = player

        replacement_values = {}

        for position, player_name in replacement_players.items():
            player = self.projections.loc[self.projections.Player == player_name]
            replacement_values[position] = player["FPTS"].tolist()[0]

        projections = self.projections.loc[
            self.projections.Position.isin(["QB", "RB", "WR", "TE"])
        ]
        projections["VOR"] = projections.apply(
            lambda row: row["FPTS"] - replacement_values.get(row["Position"]), axis=1
        )
        projections["VOR Rank"] = projections["VOR"].rank(ascending=False).astype(int)
        projections = projections.sort_values("VOR", ascending=False)

        complete_df = projections.merge(
            self.adp, how="left", on=["Player", "Position"]
        )[:200].dropna()
        complete_df["ADP Rank"] = complete_df["ADP"].rank().astype(int)
        complete_df["Sleeper Score"] = complete_df["ADP Rank"] - complete_df["VOR Rank"]
        complete_df = complete_df[
            ["Player", "Position", "VOR Rank", "ADP Rank", "Sleeper Score"]
        ]

        player_tiers = self.tiering_players_all()

        complete_df = pd.merge(complete_df, player_tiers, how="left", on="Player")

        return complete_df


def main(output_path: str, excel: bool = True, json: bool = False):
    today = date.today().strftime("%m_%d_%y")
    scoring = ["STD", "HALF", "PPR"]

    if excel:
        path = os.path.join(output_path, f"draftboards_{today}.xlsx")
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            for score in scoring:
                df = DraftBoard(score).get_draft_board()
                df.to_excel(writer, sheet_name=score, index=False)

    if json:
        for score in scoring:
            df = DraftBoard(score).get_draft_board()
            df.index += 1
            df.to_json(
                os.path.join(output_path, f"draftboard_{score}.json"),
                orient="records",
            )

    print(f"Output saved in {output_path}/")


if __name__ == "__main__":
    # pull_draft_boards(os.path.join(os.getcwd(), "root/backend/app/data/"))
    main("/Users/tylerbakely/Desktop/draftboards")

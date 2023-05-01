import json


def fmt(i):
    return int(i * 10000) / 100


DIFF_DISTANCE = 1


if __name__ == "__main__":
    with open('./data/index.json') as f_index:
        idx = json.load(f_index)
        preds = idx['predictions']
        diff_comp = [preds[-1 - DIFF_DISTANCE], preds[-1]]
        print(f"Comparing {','.join(diff_comp)}")

    teams = set()  # make sure there's no new sudden teams (or missing teams)
    qual_shifts = {}
    for be_af, sign in zip(diff_comp, [-1, 1]):
        with open(f"./data/{be_af}") as fin:
            pred = json.load(fin)
            its = pred['iterations']
            for team, outcomes in pred['team_outcomes'].items():
                if sign == -1:
                    teams.add(team)
                elif sign == 1:
                    assert team in teams
                    teams.remove(team)

                val = qual_shifts.get(team, list())
                val.append(outcomes['points_qual'] / its)
                qual_shifts[team] = val

    assert len(teams) == 0
    print("Shifts in direct (points) qual. %")
    for team, shift in sorted(qual_shifts.items(), key=lambda x: abs(x[1][1]-x[1][0]), reverse=True):
        print(f"{team}: {fmt(shift[1] - shift[0])}% ({fmt(shift[0])}% -> {fmt(shift[1])}%) ")

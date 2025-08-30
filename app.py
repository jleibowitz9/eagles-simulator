# simulator.py

# --- BEGIN: Simulation API function ---
def run_simulation(eagles_results_input, weight_input):
    import itertools

    # Use the values passed in from the UI
    eagles_results = eagles_results_input
    weight = weight_input

    # Reuse module-level data so VS Code prints and the app match
    global picks_dict, division_weeks, predicted_points, actual_points

    total_weeks = len(eagles_results)

    # Current points from games already decided in eagles_results
    current_points = {name: 0 for name in picks_dict}
    for name, picks in picks_dict.items():
        for week in range(total_weeks):
            if picks[week] == eagles_results[week]:
                current_points[name] += 1

    week_number = sum(1 for r in eagles_results if r != 'A')
    week_range = total_weeks - week_number
    outcomes = [list(x) for x in itertools.product(['W', 'L'], repeat=week_range)]
    week_number_wins = sum(1 for r in eagles_results[:week_number] if r == 'W')

    def outcome_chance_weighted(outcome):
        chance = 1.0
        for i in range(week_number, total_weeks):
            p = weight[i]
            chance *= (p if outcome[i - week_number] == 'W' else (1 - p))
        return chance

    # Tiebreaker expectations (from the same data as your VS Code run)
    predicted_wins = {name: picks.count('W') for name, picks in picks_dict.items()}
    predicted_division_wins = {
        name: sum(1 for i in division_weeks if picks_dict[name][i] == 'W')
        for name in picks_dict
    }

    weighted_tally = {name: 0.0 for name in picks_dict}
    straight_tally = {name: 0.0 for name in picks_dict}

    for outcome in outcomes:
        chance = outcome_chance_weighted(outcome)

        # Score each participant for this outcome
        tally = {name: current_points[name] for name in picks_dict}
        for name, predictions in picks_dict.items():
            for week in range(week_number, total_weeks):
                if predictions[week] == outcome[week - week_number]:
                    tally[name] += 1

        max_score = max(tally.values())
        tied = [n for n, sc in tally.items() if sc == max_score]

        if len(tied) == 1:
            weighted_tally[tied[0]] += chance * 100.0
            straight_tally[tied[0]] += 1.0
            continue

        # 1) final record tiebreaker
        actual_wins = outcome.count('W') + week_number_wins
        best_diff = min(abs(predicted_wins[n] - actual_wins) for n in tied)
        winners = [n for n in tied if abs(predicted_wins[n] - actual_wins) == best_diff]

        # 2) division record tiebreaker
        if len(winners) > 1:
            actual_div_wins = sum(
                (eagles_results[i] == 'W') if i < week_number else (outcome[i - week_number] == 'W')
                for i in division_weeks
            )
            best_div_diff = min(abs(predicted_division_wins[n] - actual_div_wins) for n in winners)
            winners = [n for n in winners if abs(predicted_division_wins[n] - actual_div_wins) == best_div_diff]

        # 3) points tiebreaker
        if len(winners) > 1:
            best_pts_diff = min(abs(predicted_points[n] - actual_points) for n in winners)
            winners = [n for n in winners if abs(predicted_points[n] - actual_points) == best_pts_diff]

        share = 1.0 / len(winners)
        for w in winners:
            weighted_tally[w] += chance * 100.0 * share
            straight_tally[w] += share

    # Convert tallies to percentage lists in name-order
    names_in_order = list(picks_dict.keys())
    weighted_list = [round(weighted_tally[n], 1) for n in names_in_order]
    straight_list = [round((straight_tally[n] / len(outcomes)) * 100.0, 1) for n in names_in_order]
    return {"weighted": weighted_list, "straight": straight_list}
# --- END: Simulation API function ---
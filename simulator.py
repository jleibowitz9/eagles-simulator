# Import itertools

import itertools

# Participant picks

picks_dict = {
'amir':     ['W',	'W',	'W',	'W',	'L',	'W',	'L',	'W',	'L',    'W',	'L',	'L',	'W',	'W',	'W',	'L',	'W'],
'andy':     ['L',	'W',	'L',	'W',	'L',	'W',	'L',	'W',	'L',	'W',	'W',	'L',	'W',	'W',	'L',	'W',	'W'],
'buhduh':   ['L',	'W',	'W',	'W',	'W',	'W',	'L',	'W',	'W',	'W',	'W',	'L',	'W',	'W',	'L',	'L',	'W'],
'emer':     ['W',	'W',	'W',	'L',	'L',	'W',	'L',	'W',	'L',	'W',	'W',    'L',	'W',	'W',	'W',	'W',	'W'],
'hanan':    ['W',	'W',	'L',	'W',	'W',	'W',	'L',	'W',	'L',    'W',	'L',	'L',	'W',	'W',	'W',	'W',	'W'],
'jacob':    ['L',	'W',	'W',	'W',	'W',	'W',	'L',	'W',	'W',	'W',	'L',	'W',	'W',	'L',	'W',	'L',	'W'],
'jay':      ['W',   'W',    'W',    'W',	'L',	'W',	'W',	'W',	'L',	'W',	'W',	'L',	'W',	'W',	'W',	'W',	'W'],
'jen':      ['W',	'W',	'L',	'W',	'L',	'W',	'L',	'W',	'L',	'W',	'W',	'L',	'W',	'L',	'W',	'W',	'W'],
'marsha':   ['L',	'W',	'W',	'W',	'L',	'W',	'L',	'L',	'W',	'W',	'L',	'L',	'W',	'W',	'W',	'W',	'W'],
'nathan':   ['L',	'W',	'W',	'W',	'W',	'W',    'W',	'L',	'L',	'W',	'W',	'L',    'W',	'W',	'W',	'W',	'W'],
'pop':      ['W',	'L',	'W',	'W',	'W',	'W',	'L',	'L',	'L',	'W',	'W',	'L',	'W',	'L',	'W',	'L',	'W'],
'sarah':    ['W',	'W',	'L',	'W',	'W',	'W',	'L',	'W',	'W',	'W',	'L',	'L',	'W',	'W',	'W',	'L',	'W']
}

# Pre-calculate predicted final record for tiebreaker
predicted_wins = {name: picks.count('W') for name, picks in picks_dict.items()}

# Indices (0-based) of intra-division games vs. Cowboys, Commanders, Giants (6 total); adjust as needed
division_weeks = [5, 8, 9, 14, 15, 16]

# Pre-calculate predicted division record for second tiebreaker
predicted_division_wins = {
    name: sum(1 for i in division_weeks if picks[i] == 'W')
    for name, picks in picks_dict.items()
}

# Pre-calculate predicted total points guess for final tiebreaker
predicted_points = {
    'amir': 450,
    'andy':   460,
    'buhduh': 440,
    'emer': 400,
    'hanan': 400,
    'jacob': 400,
    'jay': 400,
    'jen': 400,
    'marsha': 400,
    'nathan': 400,
    'pop': 400,
    'sarah': 400,
}

# Actual total points scored by the Eagles at season end
actual_points = 460  # set to the real total when known

# Eagles in-season performance (W for win; L for loss; A for not played yet)

eagles_results = [
    'W', # 0 Packers
    'L', # 1 Falcons
    'W', # 2 Saints
    'L', # 3 Bucs
    'W', # 4 Browns
    'W', # 5 Giants
    'W', # 6 Bengals
    'W', # 7 Jags
    'W', # 8 Cowboys
    'W', # 9 Comms
    'W', # 10 Rams
    'W', # 11 Ravens
    'W', # 12 Panthers
    'W', # 13 Steelers
    'L', # 14 Comms
    'W', # 15 Cowboys
    'W'  # 16 Giants
]

# Number of games in this season (auto-adjusts for mini-season testing)
total_weeks = len(eagles_results)

# Create points tally

tally_total = {'amir':0, 'andy':0, 'buhduh':0, 'emer':0, 'hanan':0, 'jacob':0, 'jay':0, 'jen':0, 'marsha':0, 'nathan':0, 'pop':0, 'sarah':0}
weight = {
    0:  .500, # Packers
    1:  .626, # Falcons
    2:  .487, # Saints
    3:  .610, # Bucs
    4:  .671, # Browns
    5:  .641, # Giants
    6:  .499, # Bengals
    7:  .685, # Jags
    8:  .597, # Cowboys
    9:  .584, # Comms
    10: .587, # Rams
    11: .413, # Ravens
    12: .851, # Panthers
    13: .610, # Steelers
    14: .577, # Comms
    15: .768, # Cowboys
    16: .834  # Giants
    }

# Tally competitors' points

current_points = {'amir':0, 'andy':0, 'buhduh':0, 'emer':0, 'hanan':0, 'jacob':0, 'jay':0, 'jen':0, 'marsha':0, 'nathan':0, 'pop':0, 'sarah':0}

for name,picks in picks_dict.items():
    for week in range(total_weeks):
        if picks[week] == eagles_results[week]:
            current_points[name] += 1

# Calculate current week

week_number = 0
for week in range(total_weeks):
    if eagles_results[week] != 'A':
        week_number += 1

week_range = total_weeks - week_number

# Create list of all possible outcomes

l = ['W', 'L']
outcomes = [list(i) for i in itertools.product(l, repeat = week_range)]
print('')
print('Remaining outcomes:', len(outcomes))
print('')
print('----------')


# WEIGHTED -------------------------------------------------------------------------------------------

week_number_wins = sum(1 for result in eagles_results[:week_number] if result == 'W')

# Define function
def outcome_chance_weighted(outcome):
    chance = 1
    for i in range(week_number, total_weeks):
        if outcome[i - week_number] == 'W':
            chance = chance * weight[i]
        else:
            chance = chance * (1 - weight[i])
    return chance

# Iterate through each one

for outcome in outcomes:
    tally_dict = {}
    chance = outcome_chance_weighted(outcome)
    for name,predictions in picks_dict.items():
        tally_dict[name] = current_points[name] 
        for week in range(week_number, total_weeks):
            if predictions[week] == outcome[week - week_number]:
                tally_dict[name] += 1
    max_value = max(tally_dict.values())
    tied_names = [name for name, matches in tally_dict.items() if matches == max_value]
    if len(tied_names) == 1:
        tally_total[tied_names[0]] += chance * 100
    elif len(tied_names) > 1:
        print(f"[Weighted Tie] Tied on correct picks: {tied_names}")
        actual_wins = outcome.count('W') + week_number_wins
        closest_diff = min(abs(predicted_wins[name] - actual_wins) for name in tied_names)
        winners = [name for name in tied_names if abs(predicted_wins[name] - actual_wins) == closest_diff]
        # SECOND TIEBREAKER: division record closeness
        if len(winners) > 1:
            # Calculate actual division wins for this simulated outcome
            actual_division_wins = sum(
                (eagles_results[i] == 'W') if i < week_number else (outcome[i-week_number] == 'W')
                for i in division_weeks
            )
            closest_div_diff = min(
                abs(predicted_division_wins[name] - actual_division_wins)
                for name in winners
            )
            winners = [
                name for name in winners
                if abs(predicted_division_wins[name] - actual_division_wins) == closest_div_diff
            ]
        # FINAL TIEBREAKER: total points scored closeness
        if len(winners) > 1:
            closest_point_diff = min(
                abs(predicted_points[name] - actual_points)
                for name in winners
            )
            winners = [
                name for name in winners
                if abs(predicted_points[name] - actual_points) == closest_point_diff
            ]
        for winner in winners:
            tally_total[winner] += chance * 100 / len(winners)

print('')
print('Weighted:')
print('')

for person,percent in tally_total.items(): # Percent
    print(person, ':', round(percent,1), '%')

print('')
print('W COPY: ')
print('')

copy_weighted = []
for percent in tally_total.values():
    copy_weighted.append(round(percent,1))

print(copy_weighted)

print('')
print('----------')



# STRAIGHT -------------------------------------------------------------------------------------------------

# Iterate through each one

tally_total = {'amir':0, 'andy':0, 'buhduh':0, 'emer':0, 'hanan':0, 'jacob':0, 'jay':0, 'jen':0, 'marsha':0, 'nathan':0, 'pop':0, 'sarah':0}

for outcome in outcomes:
    tally_dict = {}
    for name,predictions in picks_dict.items():
        tally_dict[name] = current_points[name]
        for week in range(week_number, total_weeks):
            if predictions[week] == outcome[week - week_number]:
                tally_dict[name] += 1
    max_value = max(tally_dict.values())
    tied_names = [name for name, matches in tally_dict.items() if matches == max_value]
    if len(tied_names) == 1:
        tally_total[tied_names[0]] += 1
    elif len(tied_names) > 1:
        print(f"[Straight Tie] Tied on correct picks: {tied_names}")
        actual_wins = outcome.count('W') + week_number_wins
        closest_diff = min(abs(predicted_wins[name] - actual_wins) for name in tied_names)
        winners = [name for name in tied_names if abs(predicted_wins[name] - actual_wins) == closest_diff]
        # SECOND TIEBREAKER: division record closeness
        if len(winners) > 1:
            # Calculate actual division wins for this simulated outcome
            actual_division_wins = sum(
                (eagles_results[i] == 'W') if i < week_number else (outcome[i-week_number] == 'W')
                for i in division_weeks
            )
            closest_div_diff = min(
                abs(predicted_division_wins[name] - actual_division_wins)
                for name in winners
            )
            winners = [
                name for name in winners
                if abs(predicted_division_wins[name] - actual_division_wins) == closest_div_diff
            ]
        # FINAL TIEBREAKER: total points scored closeness
        if len(winners) > 1:
            closest_point_diff = min(
                abs(predicted_points[name] - actual_points)
                for name in winners
            )
            winners = [
                name for name in winners
                if abs(predicted_points[name] - actual_points) == closest_point_diff
            ]
        for winner in winners:
            tally_total[winner] += 1 / len(winners)

print('')
print('Straight:')
print('')

number_outcomes = len(outcomes) # Percent
percentages = {person:(outcome/number_outcomes)*100 for person,outcome in tally_total.items()}

for person,percent in percentages.items():
    print(person, ':', round(percent,1), '%')

print('')
print('S COPY: ')
print('')

copy_straight = []
for percent in percentages.values():
    copy_straight.append(round(percent,1))

print(copy_straight)

print('')
print('----------')
print('')
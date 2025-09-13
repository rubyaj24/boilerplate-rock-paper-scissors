import random

def player(prev_play, opponent_history=[]):
    if prev_play:
        opponent_history.append(prev_play)

    # Play "R" for the first few moves
    if len(opponent_history) < 5:
        return "R"

    # Check for a 5-move repeating pattern (Abbey's length)
    pattern_size = 5
    if len(opponent_history) >= pattern_size * 2:
        pattern = opponent_history[-pattern_size:]
        prev_pattern = opponent_history[-2*pattern_size:-pattern_size]
        if pattern == prev_pattern:
            # Predict Abbey's next move in the pattern
            idx = len(opponent_history) % pattern_size
            predicted = pattern[idx]
            counter_moves = {"R": "P", "P": "S", "S": "R"}
            return counter_moves[predicted]

    # Fallback: bigram prediction
    patterns = {}
    for i in range(len(opponent_history) - 2):
        key = (opponent_history[i], opponent_history[i + 1])
        next_move = opponent_history[i + 2]
        if key not in patterns:
            patterns[key] = {"R": 0, "P": 0, "S": 0}
        patterns[key][next_move] += 1

    last_two = tuple(opponent_history[-2:])
    if last_two in patterns and sum(patterns[last_two].values()) > 0:
        predicted = max(patterns[last_two], key=patterns[last_two].get)
    else:
        # Fallback: randomize between countering most common and random
        from collections import Counter
        counts = Counter(opponent_history)
        predicted = counts.most_common(1)[0][0]
        if random.random() < 0.7:
            counter_moves = {"R": "P", "P": "S", "S": "R"}
            return counter_moves[predicted]
        else:
            return random.choice(["R", "P", "S"])

    counter_moves = {"R": "P", "P": "S", "S": "R"}
    return counter_moves[predicted]

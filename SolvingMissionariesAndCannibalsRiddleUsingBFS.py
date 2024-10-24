from collections import deque

class State:
    def __init__(self, left_m, left_c, boat, right_m, right_c, parent=None):
        self.left_m = left_m
        self.left_c = left_c
        self.boat = boat
        self.right_m = right_m
        self.right_c = right_c
        self.parent = parent

    def __eq__(self, other):
        return self.left_m == other.left_m and self.left_c == other.left_c and self.boat == other.boat and self.right_m == other.right_m and self.right_c == other.right_c

    def __hash__(self):
        return hash((self.left_m, self.left_c, self.boat, self.right_m, self.right_c))

    def is_valid(self):
        if self.left_m < 0 or self.left_c < 0 or self.right_m < 0 or self.right_c < 0:
            return False
        if (self.left_m < self.left_c and self.left_m > 0) or (self.right_m < self.right_c and self.right_m > 0):
            return False
        return True

    def is_goal(self):
        return self.left_m == 0 and self.left_c == 0

    def successors(self):
        successors = []
        if self.boat == 'left':
            if self.left_m >= 2:
                successors.append(State(self.left_m - 2, self.left_c, 'right', self.right_m + 2, self.right_c, self))
            if self.left_m >= 1:
                successors.append(State(self.left_m - 1, self.left_c, 'right', self.right_m + 1, self.right_c, self))
            if self.left_c >= 2:
                successors.append(State(self.left_m, self.left_c - 2, 'right', self.right_m, self.right_c + 2, self))
            if self.left_c >= 1:
                successors.append(State(self.left_m, self.left_c - 1, 'right', self.right_m, self.right_c + 1, self))
            if self.left_m >= 1 and self.left_c >= 1:
                successors.append(State(self.left_m - 1, self.left_c - 1, 'right', self.right_m + 1, self.right_c + 1, self))
        else:
            if self.right_m >= 2:
                successors.append(State(self.left_m + 2, self.left_c, 'left', self.right_m - 2, self.right_c, self))
            if self.right_m >= 1:
                successors.append(State(self.left_m + 1, self.left_c, 'left', self.right_m - 1, self.right_c, self))
            if self.right_c >= 2:
                successors.append(State(self.left_m, self.left_c + 2, 'left', self.right_m, self.right_c - 2, self))
            if self.right_c >= 1:
                successors.append(State(self.left_m, self.left_c + 1, 'left', self.right_m, self.right_c - 1, self))
            if self.right_m >= 1 and self.right_c >= 1:
                successors.append(State(self.left_m + 1, self.left_c + 1, 'left', self.right_m - 1, self.right_c - 1, self))
        return [state for state in successors if state.is_valid()]

def breadth_first_search(start_state):
    if start_state.is_goal():
        return start_state
    frontier = deque([start_state])
    explored = set()
    while frontier:
        state = frontier.popleft()
        if state.is_goal():
            return state
        explored.add(state)
        for successor in state.successors():
            if successor not in explored and successor not in frontier:
                frontier.append(successor)
    return None

def trace_solution(goal_state):
    solution = []
    state = goal_state
    while state:
        solution.append(state)
        state = state.parent
    return solution[::-1]

def main():
    left_m = int(input("Enter the number of missionaries on the left side: "))
    left_c = int(input("Enter the number of cannibals on the left side: "))
    start_state = State(left_m, left_c, 'left', 0, 0)
    goal_state = breadth_first_search(start_state)
    if goal_state:
        solution = trace_solution(goal_state)
        print("Solution found with", len(solution) - 1, "moves:")
        for i, state in enumerate(solution):
            print("Move", i, ":")
            print("Left:", state.left_m, "missionaries,", state.left_c, "cannibals")
            print("Boat:", state.boat)
            print("Right:", state.right_m, "missionaries,", state.right_c, "cannibals")
            print()
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()

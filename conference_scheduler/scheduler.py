import pulp
import conference_scheduler.parameters as params
from conference_scheduler.resources import ScheduledItem


def is_valid_schedule(schedule):
    if len(schedule) == 0:
        return False
    return True


def solution(shape, events, slots, sessions, constraints=None, existing=None):
    problem = pulp.LpProblem()
    X = params.variables(shape)
    session_array = params.session_array(sessions)
    tag_array = params.tag_array(events)
    availability_array = params.availability_array(events, slots)

    for constraint in params.constraints(shape, session_array,
                                         tag_array,
                                         availability_array, X):
        problem += constraint
    if constraints is not None:
        for constraint in constraints:
            problem += constraint
    status = problem.solve()
    if status == 1:
        return (
            item for item, variable in X.items()
            if variable.value() > 0
        )
    else:
        raise ValueError('No valid solution found')


def schedule(events, slots, constraints=None, existing=None):
    shape = params.Shape(len(events), len(slots))
    return (
        ScheduledItem(
            event=events[item[0]],
            slot=slots[item[1]]
        )
        for item in solution(shape, constraints, existing)
    )

import datetime

from approvaltests import (
    verify,
    Options,
    run_all_combinations,
    verify_logging_for_all_combinations,
)
from approvaltests.utilities.logger.simple_logger import SimpleLogger


def test_warnings():
    def scrubber(text: str) -> str:
        return text.replace(__file__, "test_simple_logger.py")

    output = SimpleLogger.log_to_string()
    SimpleLogger._logger.log_stack_traces = True
    text = "EVERYTHING IS AWFUL!!!!!!"
    try:
        raise Exception("EVERYTHING IS exceptionally AWFUL!!!!!!")
    except Exception as e:
        exception = e
    SimpleLogger.warning(text)
    SimpleLogger.warning(exception)
    SimpleLogger.warning(text, exception)
    verify(output, options=Options().with_scrubber(scrubber))


def log_from_inner_method():
    with SimpleLogger.use_markers():
        name = "Example"
        SimpleLogger.variable("name", name)
        for _ in range(0, 142):
            SimpleLogger.hour_glass()


def test_standard_logger():
    output = SimpleLogger.log_to_string()
    with SimpleLogger.use_markers() as m:
        log_from_inner_method()

    verify(output)


def test_timestamps():
    output = SimpleLogger.log_to_string()
    count = -1

    def create_applesauce_timer():
        dates = [
            datetime.datetime.fromtimestamp(0.0),
            datetime.datetime.fromtimestamp(0.5),
            datetime.datetime.fromtimestamp(2.0),
            datetime.datetime.fromtimestamp(1050),
            datetime.datetime.fromtimestamp(1052),
        ]
        nonlocal count
        count = count + 1
        return dates[count]

    SimpleLogger._logger.timer = create_applesauce_timer
    SimpleLogger.show_timestamps(True)
    SimpleLogger.event("1")
    SimpleLogger.event("2")
    SimpleLogger.event("3")
    SimpleLogger.event("4")
    SimpleLogger.warning(exception=Exception("Oh no you didn't!"))
    verify(output)


def test_variable():
    output = SimpleLogger.log_to_string()
    with SimpleLogger.use_markers():
        SimpleLogger.variable("dalmatians", 101, show_types=True)
        SimpleLogger.variable("dalmatians", 101, show_types=False)
    verify(output)


def test_variable_with_list():
    output = SimpleLogger.log_to_string()
    with SimpleLogger.use_markers():
        names = ["Jacqueline", "Llewellyn"]
        SimpleLogger.variable("names", names, show_types=True)
        SimpleLogger.variable("names", names, show_types=False)
    verify(output)


def verify_toggle(toggle_name, toggle):
    SimpleLogger.show_all(True)
    SimpleLogger.event(f"Toggle Off {toggle_name}")
    toggle(False)
    log_everything()


def test_switching() -> None:
    output = SimpleLogger.log_to_string()

    verify_toggle("None", lambda a: SimpleLogger.show_all(True)),
    verify_toggle("All", SimpleLogger.show_all),
    verify_toggle("Query", SimpleLogger.show_queries),
    verify_toggle("Message", SimpleLogger.show_messages),
    verify_toggle("Variable", SimpleLogger.show_variables),
    verify_toggle("Hour Glass", SimpleLogger.show_hour_glass),
    verify_toggle("Markers", SimpleLogger.show_markers),
    verify_toggle("Events", SimpleLogger.show_events),

    verify(output)


def log_everything() -> None:
    with SimpleLogger.use_markers():
        SimpleLogger.query("Select * from people")
        SimpleLogger.variable("Nonsense", "foo")
        SimpleLogger.event("Testing")
        SimpleLogger.message("Something random")
        for a in range(1, 13):
            SimpleLogger.hour_glass()
        try:
            infinity = 1 / 0
        except Exception as e:
            SimpleLogger.warning(exception=e)


def function_to_run(color, number) -> None:
    with SimpleLogger.use_markers():
        SimpleLogger.variable("color", color)
        SimpleLogger.variable("number", number)
        if number == "brie":
            raise Exception("AHHHHHH!")


def test_use_markers_with_raised_exception() -> None:
    def throw_exception():
        with SimpleLogger.use_markers():
            raise Exception("Everything is awflu!!?")

    output = SimpleLogger.log_to_string()
    try:
        throw_exception()
    except BaseException as e:
        SimpleLogger.warning(e)
    verify(output)


def test_run_combinations() -> None:
    output = SimpleLogger.log_to_string()
    run_all_combinations(function_to_run, [["red", "blue"], ["one", "two", "brie"]])
    verify(output)


def test_verify_logging_for_all_combinations() -> None:
    verify_logging_for_all_combinations(
        function_to_run, [["red", "blue"], ["one", "two", "brie"]]
    )

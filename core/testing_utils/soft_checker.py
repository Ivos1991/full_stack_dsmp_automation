import traceback
from contextlib import contextmanager
from assertpy import assert_that as assertpy_assert_that
from playwright.sync_api import expect as playwright_expect


class SoftChecker:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def _capture_location(self) -> str:
        stack = traceback.extract_stack(limit=10)
        for frame in reversed(stack):
            if "soft_checker" not in frame.filename:
                return f"{frame.filename}:{frame.lineno}"
        return "unknown location"

    def expect(self, locator, message: str | None = None):
        checker = self

        class Proxy:
            def __getattr__(self, method_name):
                method = getattr(playwright_expect(locator), method_name)

                def wrapper(*args, **kwargs):
                    try:
                        return method(*args, **kwargs)
                    except AssertionError as error:
                        checker.errors.append(f"{checker._capture_location()}: {message or str(error)}")

                return wrapper

        return Proxy()

    def assert_that(self, *args):
        checker = self
        assertion = assertpy_assert_that(*args)

        class Proxy:
            def __getattr__(self, method_name):
                method = getattr(assertion, method_name)

                def wrapper(*wrapper_args, **wrapper_kwargs):
                    try:
                        return method(*wrapper_args, **wrapper_kwargs)
                    except AssertionError as error:
                        checker.errors.append(f"{checker._capture_location()}: {error}")

                return wrapper

        return Proxy()

    def raise_if_any(self) -> None:
        if self.errors:
            formatted_errors = "\n----\n".join(f"{index + 1}. {message}" for index, message in enumerate(self.errors))
            raise AssertionError(f"soft assertion failures:\n{formatted_errors}")


@contextmanager
def soft_checker():
    checker = SoftChecker()
    yield checker
    checker.raise_if_any()

def main() -> None:
    from .cli import debug

    debug(windows_expand_args=False)  # type: ignore[misc]


if __name__ == "__main__":
    main()

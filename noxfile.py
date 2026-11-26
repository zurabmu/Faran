import nox

nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True


def install_test_environment(session: nox.Session, *extras: str) -> None:
    session.run_install(
        "uv",
        "sync",
        "--frozen",
        "--no-default-groups",
        "--group=test",
        *(f"--extra={extra}" for extra in extras),
        env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location},
    )


@nox.session(python="3.13")
def test_without_jax(session: nox.Session) -> None:
    install_test_environment(session)
    session.run(
        "pytest",
        "--tb=short",
        "--ignore=tests/benchmarks",
        "--ignore=tests/test_docsite",
        *session.posargs,
    )


@nox.session(python="3.13")
def test_full(session: nox.Session) -> None:
    install_test_environment(session, "jax")
    session.run(
        "pytest",
        "--tb=short",
        "--ignore=tests/benchmarks",
        "--ignore=tests/test_docsite",
        *session.posargs,
        env={"NEEDY_STRICT": "true"},
    )

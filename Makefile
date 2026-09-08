.PHONY: all install run debug clean fclean lint lint-strict

UV = @uv run
UV_PYTHON = @uv run python -m
MAIN = main.py
CACHE = __pycache__ src/__pycache__ .mypy_cache src/.mypy_cache mazegenerator-00001/__pycache__ mazegenerator-00001/.mypy_cache
MYPYFLAGS = --warn-return-any --warn-unused-ignores\
			  --ignore-missing-imports --disallow-untyped-defs\
			  --check-untyped-defs

all: run

run:
	$(UV_PYTHON) $(MAIN)

clean:
	rm -rf $(CACHE)

fclean:
	rm -rf $(CACHE)
	rm -rf .venv

install:
	@uv sync

debug:
	$(UV_PYTHON) pdb $(MAIN)

lint:
	$(UV) flake8 .
	$(UV) mypy . $(MYPYFLAGS)

lint-strict:
	$(UV) flake8 .
	$(UV) mypy . --strict
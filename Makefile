.PHONY: all install run debug clean fclean lint lint-strict

UV = @uv run
UV_PYTHON = @uv run python
MAIN = pac-man.py
CACHE = __pycache__ .mypy_cache \
		src/__pycache__ src/.mypy_cache\
		mazegenerator/__pycache__ mazegenerator/.mypy_cache
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
	uv sync
	uv pip install mlx-2.2-py3-none-any.whl

debug:
	$(UV_PYTHON) pdb $(MAIN)

lint:
	$(UV) flake8 .
	$(UV) mypy . $(MYPYFLAGS)

lint-strict:
	$(UV) flake8 .
	$(UV) mypy . --strict
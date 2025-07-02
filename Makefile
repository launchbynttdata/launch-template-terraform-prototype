test:
	@-uv run pytest

render:
	uv run copier . temp/ --trust

clean:
	@-rm -rf temp/

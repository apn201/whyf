# WHY THE F? - build targets
# Windows: run these from Git Bash, or copy the command out of the recipe.

PY := python

.PHONY: help corpus synthetic cards progress validate publishable check test deploy clean

help:
	@echo "corpus    re-parse the private sources (needs private/)"
	@echo "synthetic regenerate the public corpus"
	@echo "publishable  check nothing from private/ leaked into the tree"
	@echo "cards     regenerate skeletons from the corpus (never overwrites your writing)"
	@echo "progress  writing scoreboard"
	@echo "validate  schema + referential integrity across the whole corpus"
	@echo "check     mapping + validate + tests. run before every commit."
	@echo "test      pytest"
	@echo "deploy    cdk deploy (needs AWS_PROFILE=whyf and docs/AWS-SETUP.md done)"

synthetic:
	$(PY) tools/gen_synthetic.py

publishable:
	$(PY) tools/check_publishable.py

corpus:
	$(PY) tools/parse_q2.py
	$(PY) tools/parse_annex.py
	$(PY) tools/parse_benchmarks.py
	$(PY) tools/corpus_map.py

cards:
	$(PY) tools/corpus_map.py
	$(PY) tools/gen_skeletons.py
	$(PY) tools/gen_library.py

progress:
	$(PY) tools/validate_cards.py --progress

validate:
	$(PY) tools/validate_cards.py

check: validate publishable test
	$(PY) tools/corpus_map.py

test:
	$(PY) -m pytest -q

deploy:
	cd infra && npx cdk deploy --profile $${AWS_PROFILE:-whyf}

clean:
	rm -rf cdk.out .pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +

#!/usr/bin/env bash

# ==============================================================================
# Smoke-Fixture Consistency Guard
#
# Every environment's mounted dataset (data/dev, data/staging) embeds the smoke
# rows (year 1970) so that the init-deploy smoke phase can run in that env. The
# smoke assertions are pinned to the canonical fixture (data/smoke-test), so the
# embedded 1970 rows MUST stay byte-identical to it (content AND line endings).
#
# This guard diffs the 1970 rows of each env file against the canonical fixture
# and fails CI on any drift (e.g. a stray CRLF or an edited value).
#
# Usage: ./scripts/check-data-fixtures.sh
# ==============================================================================

source "$(dirname "$0")/lib/common.sh"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$SCRIPT_DIR/../data"
FIXTURE="$DATA_DIR/smoke-test/covid_data.csv"
ENV_FILES=("$DATA_DIR/dev/covid_data.csv" "$DATA_DIR/staging/covid_data.csv")

# The smoke window lives entirely in calendar year 1970 (date column: YYYY/MM/DD).
smoke_rows() { grep ',1970/' "$1"; }

main() {
    log_info "========== Smoke-Fixture Consistency Guard =========="

    if [[ ! -s "$FIXTURE" ]]; then
        log_error "Canonical fixture missing or empty: $FIXTURE"
        exit 1
    fi

    local failed=0
    for env_file in "${ENV_FILES[@]}"; do
        if [[ ! -f "$env_file" ]]; then
            log_error "Env dataset not found: $env_file"
            failed=1
            continue
        fi
        if diff <(smoke_rows "$env_file") <(smoke_rows "$FIXTURE") > /dev/null; then
            log_success "1970 rows match canonical fixture: $env_file"
        else
            log_error "1970 rows DRIFTED from canonical fixture: $env_file"
            diff <(smoke_rows "$env_file") <(smoke_rows "$FIXTURE") || true
            failed=1
        fi
    done

    if [[ "$failed" -ne 0 ]]; then
        log_error "Smoke-fixture consistency check FAILED."
        exit 1
    fi
    log_success "========== All env datasets carry the canonical smoke rows =========="
}

main

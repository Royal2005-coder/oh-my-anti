#!/usr/bin/env bash
set -euo pipefail

GEMINI_CONFIG_PATH="${HOME}/.gemini/config"
echo "Installing Oh My Anti to ${GEMINI_CONFIG_PATH}..."

PLUGINS_DIR="${GEMINI_CONFIG_PATH}/plugins/oh-my-anti"
SKILLS_DIR="${GEMINI_CONFIG_PATH}/skills"
RULES_DIR="${GEMINI_CONFIG_PATH}/rules"

mkdir -p "${PLUGINS_DIR}" "${SKILLS_DIR}" "${RULES_DIR}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cp -r "${SCRIPT_DIR}/plugin.json" "${SCRIPT_DIR}/agents" "${SCRIPT_DIR}/resources" "${SCRIPT_DIR}/templates" "${SCRIPT_DIR}/scripts" "${SCRIPT_DIR}/skills" "${PLUGINS_DIR}/"

for skill in "${SCRIPT_DIR}/skills"/*; do
  if [ -d "${skill}" ]; then
    skill_name="$(basename "${skill}")"
    rm -rf "${SKILLS_DIR}/${skill_name}"
    cp -r "${skill}" "${SKILLS_DIR}/"
    echo "  -> Installed skill: ${skill_name}"
  fi
done

cp "${SCRIPT_DIR}/rules/AGENTS.md" "${RULES_DIR}/AGENTS.md"
echo "  -> Installed global intent rules: AGENTS.md"

echo "Oh My Anti successfully installed! All skills and subagents are ready."

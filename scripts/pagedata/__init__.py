"""Every generated page. scripts/gen_pages.py renders what all_pages() returns."""

from . import compare, models, usecases, prompts, status, guides, i18n


def all_pages():
    return [
        *guides.pages(),
        *compare.pages(i18n.alternates_for),
        *models.pages(),
        *usecases.pages(),
        *status.pages(),
        *prompts.pages(),
        *i18n.pages(guides.home_software_ld()),
    ]

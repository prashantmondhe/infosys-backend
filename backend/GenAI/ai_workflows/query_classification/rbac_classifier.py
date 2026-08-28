from typing import List


ROLE_PERMISSIONS: dict[str, List[str]] = {

    # -------------------------------------------------
    # Engineering
    # -------------------------------------------------

    "Software Engineer": [
        "Engineering",
    ],

    "Senior Software Engineer": [
        "Engineering",
    ],

    "DevOps Lead": [
        "Engineering",
    ],

    "Solutions Architect": [
        "Engineering",
    ],

    "Engineering Lead": [
        "Engineering",
    ],


    # -------------------------------------------------
    # Sales
    # -------------------------------------------------

    "Sales Executive": [
        "Sales",
    ],

    "Business Development Manager": [
        "Sales",
    ],

    "Account Manager": [
        "Sales",
    ],

    "Sales Enablement Lead": [
        "Sales",
    ],


    # -------------------------------------------------
    # Operations
    # -------------------------------------------------

    "Delivery Manager": [
        "Operations",
    ],

    "Operations Lead": [
        "Operations",
    ],


    # -------------------------------------------------
    # Project Management
    # -------------------------------------------------

    "PMO Lead": [
        "Project Management",
    ],


    # -------------------------------------------------
    # HR
    # -------------------------------------------------

    "HR Associate": [
        "HR",
    ],

    "HR Operations Lead": [
        "HR",
    ],


    # -------------------------------------------------
    # Management
    # -------------------------------------------------

    "Senior Manager": [
        "Engineering",
        "HR",
        "Project Management",
        "Sales",
        "Operations",
    ],
}


class QueryRBACClassifier:

    @staticmethod
    def get_allowed_departments(
        designation: str,
    ) -> List[str]:
        """
        Return departments accessible to the user's designation.
        """

        return ROLE_PERMISSIONS.get(
            designation,
            [],
        )
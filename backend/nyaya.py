class NyayaEngine:

    def check_argument(self, result):

        problems = []

        if not result["pratijna"]:
            problems.append(
                "No clear proposition was identified."
            )

        if not result["hetu"]:
            problems.append(
                "No clear reason was identified."
            )

        if not result["udaharana"]:
            problems.append(
                "No supporting example was identified."
            )

        if not result["upanaya"]:
            problems.append(
                "No application of the general rule was identified."
            )

        if not result["nigamana"]:
            problems.append(
                "No conclusion was identified."
            )

        return problems
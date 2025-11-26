class Planner:
    def plan(self, query):
        tasks = [
            {"id":1, "task":"load data"},
            {"id":2, "task":"compute roas & ctr trends"},
            {"id":3, "task":"generate hypotheses"},
            {"id":4, "task":"validate hypotheses"},
            {"id":5, "task":"generate creative suggestions"},
            {"id":6, "task":"format outputs"}
        ]
        return {"query":query, "tasks": tasks}

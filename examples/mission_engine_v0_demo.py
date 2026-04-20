from starship_protocol.engineering import ChiefEngineer, EngineeringMode
from starship_protocol.gates import GateColor
from starship_protocol.logbook import CaptainsLog
from starship_protocol.mission import Mission, MissionEngine
from starship_protocol.roles import Captain, CrewCaptain, Oxpecker, Specialist


def main() -> None:
    captain = Captain(name="Captain Ultra")
    crew_captain = CrewCaptain(name="Crew Captain Cerri", reports_to=captain.chameleon_id)
    captain.add_crew_captain(crew_captain)

    engineer = ChiefEngineer(name="Chief Engineer", reports_to=captain.chameleon_id)
    engineer.mode = EngineeringMode.BALANCED
    engineer.register_model("fast-cheap-model", strength=1, cost_tier=1)
    engineer.register_model("solid-general-model", strength=3, cost_tier=2)
    engineer.register_model("expensive-brain-model", strength=5, cost_tier=4, tags={"vision"})

    coder = Specialist(name="Chief Coder", focus_area="software", reports_to=crew_captain.chameleon_id)
    crew_captain.add_specialist(coder)
    oxpecker = Oxpecker(name="Number 1 Review", assigned_entity_id=coder.chameleon_id, reports_to=crew_captain.chameleon_id)

    mission = Mission(
        title="bootstrap starship of chameleons protocol",
        objective="create the first runnable protocol scaffold",
    )
    task = mission.add_task(
        title="build core models",
        task_type="code_generation",
        description="implement the first protocol package skeleton",
    )

    routing = engineer.choose_model(task_type=task.task_type, complexity=3)

    engine = MissionEngine()
    engine.gate_manager.set_gate("code_generation", GateColor.YELLOW)
    engine.start_mission(mission)
    engine.assign_task(task, coder.chameleon_id)

    output = coder.execute_task(task, context={"mission": mission.title, "routing": routing})
    review = oxpecker.review_output(output)
    engine.submit_output(task, {"work": output, "review": review, "routing": routing})

    log = CaptainsLog(ship_name="Starship of Chameleons")
    log.log("MISSION", f"Mission '{mission.title}' is {mission.status.value}")
    log.log("ENGINEERING", f"Selected model: {routing['chosen_model']}")
    log.log("REVIEW", f"Oxpecker approval status: {review['approved']}")

    print({
        "mission_status": mission.status.value,
        "task_status": task.status.value,
        "captain": captain.name,
        "crew_captain": crew_captain.name,
        "specialist": coder.name,
        "engineer_mode": engineer.mode.value,
        "chosen_model": routing.get("chosen_model"),
        "oxpecker": oxpecker.name,
        "review_approved": review["approved"],
        "log_entries": len(log.entries),
    })


if __name__ == "__main__":
    main()

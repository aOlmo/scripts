import os
from shutil import copyfile

try:
    os.mkdir("final/")
except OSError:
    print("Creation of the directory skipped")
else:
    print("Successfully created the directory")

final_path = "final/blocks"
opt_plan_name = "grounded_robot_plan"
deft_plan_name = "sas_plan"

domain_files = [f for f in os.listdir(".") if f.startswith("domain")]
prob_files = [f for f in os.listdir(".") if f.startswith("prob")]

count = 0
for df in domain_files:
    for pf in prob_files:
        count += 1
        final_path += str(count) + "/"

        try:
            os.mkdir(final_path)
        except OSError:
            print("Creation of the directory skipped")
        else:
            print("Successfully created the directory")

        d_name = "human-model.pddl"
        p_name = "prob.pddl"
        r_name = "robot-model.pddl"

        # Copy domain and prob files with name changed
        copyfile(df, final_path + d_name)
        copyfile(pf, final_path + p_name)

        # Copy robot model too
        copyfile("robot-model.pddl", final_path + r_name)

        # Execute FD
        os.popen("./fdplan.sh {} {}".format(final_path + r_name, final_path + p_name))

        # Change name of optimal plan to grounded_robot_plan
        copyfile(deft_plan_name, final_path + opt_plan_name)

        # Default final path name again
        final_path = "final/blocks"

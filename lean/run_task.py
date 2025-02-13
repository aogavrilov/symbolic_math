import subprocess


def run_task(pseudocode: str) -> dict:
    """Run execution of Lean pseudocode"""
    execution_success = True
    execution_error = ""
    proof = ""

    try:
        with open("example.lean", "w", encoding="utf-8") as f:
            f.write(pseudocode)
        execution_result = subprocess.run(["lake", "lean", "example.lean"], capture_output=True, text=True)
        execution_result_code = execution_result.returncode == 0
        execution_error = execution_result.stderr
        proof = execution_result.stdout
    except Exception as e:
        execution_success = False
        execution_error = e
        execution_result_code = 0

    result = {"execution_success": execution_success, "execution_error": execution_error,
              "execution_result": execution_result_code, "proof": proof}
    return result

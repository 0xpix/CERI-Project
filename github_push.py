import subprocess

def git_operations(commit_message):
    """
    Performs a series of git operations in a Google Colab environment.
    
    Args:
    commit_message (str): The commit message to use when committing changes.
    
    Returns:
    str: Outputs of the git commands.
    """
    try:
        # Set Git configuration variables
        subprocess.run(["git", "config", "--global", "user.email", "ns.chlfat@gmail.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "0xpix"], check=True)
        
        # Add all modified files to the staging area
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit the changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Push the changes to the main branch
        result = subprocess.run(["git", "push", "origin", "main"], check=True, text=True, capture_output=True)
        
        # Print a success message if the push is successful
        print("Thank you! Push operation succeeded.")
        
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"
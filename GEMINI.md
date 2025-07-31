# Git History Cleanup Plan

ver. 2.4

This document outlines the proposed plan to remove the `_skbuild/` directory (and its contents, including nested `.git` repositories) from the entire history of your Git repository. This action is intended to reduce the size of your `.git` folder and prevent future issues caused by these accidentally committed files.

Nota bene: This plan involves rewriting Git history, which is a destructive and irreversible operation. Reread Helps or use context7 or Google Search AI if unsure. User has never done this operation, so User has about 20 percent knowledge here only. (But 80 percent knowledge about what tends to go wrong if .git is ballooning, sigh...) 

---

## Plan Steps:


### Step 1: Perform a Dry Run with `git-filter-repo`

We will use `git-filter-repo` to simulate the removal of the `_skbuild/` directory from the entire history. This will show us what changes would occur without actually modifying your repository.

**Action:**
```bash
git-filter-repo --path _skbuild/ --invert-paths --dry-run
```
*   **Explanation of the command:**
    *   `git-filter-repo`: The tool we are using for history rewriting.
    *   `--path _skbuild/`: Specifies that we are targeting the `_skbuild/` directory.
    *   `--invert-paths`: This is crucial. It tells `git-filter-repo` to *keep everything EXCEPT* the paths specified by `--path`. So, in this case, it will effectively *remove* `_skbuild/` and all its contents from the history.
    *   `--dry-run`: This is a safety measure. It will run the filtering process but will not actually modify your repository. It will output a comparison of the original and filtered history, which we will review.

---

### Step 2: Review Dry Run Output

After the dry run, we will examine the output provided by `git-filter-repo`. This output will show us which commits would be modified and which files would be removed.

**Action:**
*   Gemini will not present the output of the `git-filter-repo --dry-run` command as User sees it anyway. 
*   However, we will indeed discuss the results to ensure that `_skbuild/` shall indeed be removed as expected soon and that no unintended changes are being made.
*   **Tip:** If the dry run output is unclear or you wish to investigate further, you can use diagnostic commands like `git cat-file -p <tree-hash>` (where `<tree-hash>` is identified from the dry run output) to inspect specific tree objects, or `git log --all --pretty=%H --source` combined with scripting to find commits referencing problematic trees, as discussed in previous plans.

---

### Step 3: Execute the Actual Filter  

If the dry run output looks good, and *only* after User's explicit confirmation and understanding of the implications, we will execute the `git-filter-repo` command without the `--dry-run` flag.

**Action:**
```bash
git-filter-repo --path _skbuild/ --invert-paths 
```
*   **Explanation:**
    *   The command is the same as the dry run, but without `--dry-run`, it will actually rewrite the history.
    *   **Regarding `--force`:** `git-filter-repo` often requires the `--force` flag when not run on a fresh clone, as it refuses to operate on a repository that might have uncommitted changes or other states that could lead to data loss. This is a safety mechanism built into the tool. We will discuss the necessity of this flag at this step, and it will only be used with your explicit understanding and approval.

---

### Step 4: Re-add Remote

`git-filter-repo` intentionally removes all remotes from the rewritten repository to prevent accidental pushes to the wrong remote. We need to re-add the `origin` remote so we can push the new history.

**Action:**
1.  **Retrieve original remote URL:**
    ```bash
    ORIGIN_URL=$(git remote get-url origin)
    ```
2.  **Add the remote back:**
    ```bash
    git remote add origin "$ORIGIN_URL"
    ```
*   **Explanation:** These commands first retrieve the URL of your `origin` remote (assuming it was configured before the filter) and then re-add it to the repository.

---

### Step 7: Push the Rewritten History

This is the step that updates your remote repository with the new, clean history. **This is a destructive operation on the remote and requires extreme caution.**

**Action:**
```bash
git push --all origin --prune
```
*   **Explanation:** This command pushes all branches and tags to the `origin` remote. 
    *   **Regarding `--force` for `git push`:** After a history rewrite, your local branches will have a different history than the remote branches. A regular `git push` will fail because it detects a non-fast-forward update. Therefore, `git push --force` (or the slightly safer `git push --force-with-lease`) is typically required to overwrite the remote history with your new, rewritten local history. We will discuss the necessity of this flag at this step, and it will only be used with your explicit understanding and approval.
    *   The `--prune` option will remove any remote branches or tags that no longer exist in the rewritten history.
*   **User Control Point:** I will report the output of the push. **This step requires confirmation before execution.**

---

### Step 8: Post-Filter Cleanup and Optimization

After the history rewrite is complete and gently-pushed, we need to perform several cleanup steps to remove the old, unreferenced objects and reclaim disk space.

**Action:**
1.  **Remove original refs:**

    User expresses doubt that it would work without tests: 

    ```bash
    git for-each-ref --format="%(refname)" refs/original/ | xargs -n 1 git update-ref -d
    ```
    so User proposes: 

    A. RTFM that is help or context7
    B. Test one git refs/original/ smth , probably `git update-ref -d` being that something. 
    C. Based on results of 1B construct xargs indeed, but test on second git refs/original/ smth 
    D. If B and C work, only do the full loop. 
    
    *   **Explanation:** `git-filter-repo` creates backup references under `refs/original/`. This command deletes those references, allowing the old objects to be garbage collected.

2.  **Expire all reflogs:**
    ```bash
    git reflog expire --expire=now --all
    ```
    
    User is unsure what it does so let us discuss it when we reach this step. 
    
    *   **Explanation:** The reflog keeps a history of all changes to your repository's references. This command forces the immediate expiration of all reflog entries, making old objects unreachable.
    

3.  **Garbage collect unreferenced objects:**
    ```bash
    git gc --prune=now 
    ```
    *   **Explanation:** This command performs gentle garbage collection, removing all objects that are no longer referenced by any commit or reflog entry. This is where the actual disk space will be reclaimed.

---


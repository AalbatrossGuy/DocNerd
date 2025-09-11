#! /usr/bin/python3
# Created by AG on 11-09-2025

from typing import Dict

prompts: Dict[str, str] = {
    "python": (
        "You write concise and precise google-styled python docstrings. "
        "Given a function or a code block, return ONLY the docstring content"
        "(no triple quotes or fences)."
    ),

    "rust": (
        "You write concise, precise Rustdoc comments. "
        "Return ONLY the comment body lines (no ///, no /** */). "
        "Start with a one-line summary. Use # Arguments, # Returns, and # Errors as needed."
    ),

    "others": (
        "You write concise, precise Doxygen/JSDoc-style comments for"
        " functions. Return ONLY the comment body lines (no /* */, no leading *)."
        " Start with a one-line summary. Use @param, @return, @throws (when applicable)."
    )

}

from functools import lru_cache

from app.rag.catalog_loader import load_catalog_programs

@lru_cache(maxsize=1)
def get_program_list()-> dict[str, dict]:
    programs = load_catalog_programs()
    program_list = {}

    for program in programs:
        source_id=program["source_id"]
        if source_id:
            program_list[source_id]=program
    return program_list

def get_program_by_source_id(source_id:str) -> dict[str, dict]:
    program_list = get_program_list()
    return program_list.get(source_id)

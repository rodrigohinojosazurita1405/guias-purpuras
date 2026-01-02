"""
Script para eliminar funciones duplicadas de jobs/views.py
"""

# Funciones a eliminar (líneas de inicio)
FUNCTIONS_TO_REMOVE = {
    'get_user_statistics': 1117,
    'get_user_published_jobs': 1253,
    'get_user_applied_jobs': 1355,
    'get_user_activities': 1408,
    'get_job_categories': 1821,
    'get_user_orders': 1867,
    'get_order_detail': 1971,
    'resend_invoice': 2035,
    'get_blocked_users': 2104,
    'block_user': 2167,
    'unblock_user': 2265,
    'check_if_blocked': 2306,
    'get_contract_types': 2405,
    'get_cities': 2438,
    'get_job_categories_dynamic': 2473,
}

def find_function_end(lines, start_line):
    """Encuentra el final de una función"""
    # Buscar la siguiente función o el final del archivo
    for i in range(start_line, len(lines)):
        line = lines[i]
        # Si encontramos otra definición de función al mismo nivel
        if i > start_line and line.startswith('def ') or line.startswith('@'):
            # Retroceder para incluir decorators de la siguiente función
            while i > start_line and lines[i-1].startswith('@'):
                i -= 1
            return i - 1
    return len(lines) - 1

def remove_duplicates():
    """Elimina las funciones duplicadas"""
    filepath = 'G_Jobs/jobs/views.py'

    # Leer archivo
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Convertir líneas a dict para fácil eliminación
    lines_to_keep = []
    lines_to_remove = set()

    # Identificar líneas a eliminar
    for func_name, start_line in sorted(FUNCTIONS_TO_REMOVE.items(), key=lambda x: x[1]):
        end_line = find_function_end(lines, start_line - 1)  # -1 porque las líneas empiezan en 0
        print(f"Eliminando {func_name}: líneas {start_line}-{end_line+1}")
        for line_num in range(start_line - 1, end_line + 1):
            lines_to_remove.add(line_num)

    # Mantener solo las líneas que no están marcadas para eliminar
    for i, line in enumerate(lines):
        if i not in lines_to_remove:
            lines_to_keep.append(line)

    # Escribir archivo limpio
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines_to_keep)

    print(f"\n✅ Eliminadas {len(lines_to_remove)} líneas")
    print(f"📝 Líneas originales: {len(lines)}")
    print(f"📝 Líneas finales: {len(lines_to_keep)}")
    print(f"📉 Reducción: {len(lines) - len(lines_to_keep)} líneas ({((len(lines) - len(lines_to_keep)) / len(lines) * 100):.1f}%)")

if __name__ == '__main__':
    remove_duplicates()

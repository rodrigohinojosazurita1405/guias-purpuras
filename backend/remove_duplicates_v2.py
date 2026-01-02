"""
Script mejorado para eliminar funciones duplicadas de jobs/views.py
Incluye decoradores en la eliminación
"""

# Funciones a eliminar (líneas de inicio de función, sin contar decoradores)
FUNCTIONS_TO_REMOVE = [
    'get_user_statistics',
    'get_user_published_jobs',
    'get_user_applied_jobs',
    'get_user_activities',
    'get_job_categories',
    'get_user_orders',
    'get_order_detail',
    'resend_invoice',
    'get_blocked_users',
    'block_user',
    'unblock_user',
    'check_if_blocked',
    'get_contract_types',
    'get_cities',
    'get_job_categories_dynamic',
]

def find_function_start_with_decorators(lines, func_line_num):
    """Encuentra el inicio de una función incluyendo sus decorators"""
    start = func_line_num
    # Retroceder para incluir decorators
    while start > 0 and (lines[start-1].strip().startswith('@') or lines[start-1].strip() == ''):
        start -= 1
        # Saltar líneas vacías antes de decorators
        if lines[start].strip() == '' and start > 0 and not lines[start-1].strip().startswith('@'):
            start += 1
            break
    return start

def find_function_end(lines, start_line):
    """Encuentra el final de una función"""
    # Buscar la siguiente función o el final del archivo
    for i in range(start_line + 1, len(lines)):
        line = lines[i].strip()
        # Si encontramos un decorator o función al mismo nivel de indentación
        if line.startswith('@') or line.startswith('def '):
            # Retroceder para no incluir líneas vacías
            end = i - 1
            while end > start_line and lines[end].strip() == '':
                end -= 1
            return end
    return len(lines) - 1

def remove_duplicates():
    """Elimina las funciones duplicadas"""
    filepath = 'G_Jobs/jobs/views.py'

    # Leer archivo
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"Archivo original: {len(lines)} lineas\n")

    # Encontrar líneas de las funciones a eliminar
    function_locations = {}
    for i, line in enumerate(lines):
        for func_name in FUNCTIONS_TO_REMOVE:
            if line.strip().startswith(f'def {func_name}('):
                function_locations[func_name] = i
                break

    # Identificar rangos a eliminar
    ranges_to_remove = []
    for func_name in FUNCTIONS_TO_REMOVE:
        if func_name in function_locations:
            func_line = function_locations[func_name]
            start = find_function_start_with_decorators(lines, func_line)
            end = find_function_end(lines, func_line)
            ranges_to_remove.append((start, end, func_name))
            print(f"Eliminando {func_name}: lineas {start+1}-{end+1} ({end-start+1} lineas)")

    # Ordenar rangos en orden inverso para eliminar de atrás hacia adelante
    ranges_to_remove.sort(reverse=True, key=lambda x: x[0])

    # Eliminar las líneas
    for start, end, func_name in ranges_to_remove:
        del lines[start:end+1]

    # Escribir archivo limpio
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"\nArchivo final: {len(lines)} lineas")
    print(f"Reduccion: {2506 - len(lines)} lineas")

if __name__ == '__main__':
    remove_duplicates()

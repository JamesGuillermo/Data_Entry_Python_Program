import sqlite3
import json

# ============================================================================
# STEP 1: DATABASE CREATION PARAMETERS BREAKDOWN
# ============================================================================

def create_database_step_by_step():
    """
    Shows exactly what parameters are needed to create a database
    that can store function components
    """
    
    print("=== STEP 1: CONNECTING TO DATABASE ===")
    # Parameter 1: Database filename
    database_filename = "my_functions.db"  # This will be created if it doesn't exist
    
    connection = sqlite3.connect(database_filename)
    cursor = connection.cursor()
    print(f"✓ Connected to database: {database_filename}")
    
    print("\n=== STEP 2: CREATING TABLE STRUCTURE ===")
    # Parameter 2: Table name
    table_name = "saved_functions"
    
    # Parameter 3: Column definitions (what data we need to store)
    column_definitions = [
        "id INTEGER PRIMARY KEY AUTOINCREMENT",  # Auto-numbering ID (1, 2, 3...)
        "function_name TEXT",                    # Name like "move_mouse_1" 
        "function_info TEXT"                     # JSON string with all details
    ]
    
    # Create the SQL command
    sql_command = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)})"
    print(f"SQL Command: {sql_command}")
    
    # Execute the command
    cursor.execute(sql_command)
    connection.commit()
    print(f"✓ Created table: {table_name}")
    
    connection.close()
    print("✓ Database setup complete!")

# ============================================================================
# STEP 2: FUNCTION COMPONENT BREAKDOWN  
# ============================================================================

def show_function_components():
    """
    Shows what components make up a function and how they're structured
    """
    
    print("\n=== FUNCTION COMPONENTS BREAKDOWN ===")
    
    # These are ALL the pieces of information we need to save about a function:
    function_components = {
        # Basic identification
        "name": "move_mouse_1",                    # Unique identifier
        "created_at": "2024-01-15 10:30:00",     # When it was created
        
        # Action details  
        "action_type": "move_mouse",              # What type of action
        "mouse_x": 300,                           # X coordinate for mouse
        "mouse_y": 200,                           # Y coordinate for mouse  
        "duration": 1.5,                          # How long the action takes
        
        # Display information
        "description": "Move mouse to (300, 200) - Function #1",  # Human-readable description
        "label_text": "Function 1 executed",     # Text to show on label
        "label_color": "green",                   # Color of the label
        
        # Additional metadata
        "execution_count": 0,                     # How many times it's been run
        "is_active": True                         # Whether this function is enabled
    }
    
    print("Components of a function:")
    for key, value in function_components.items():
        print(f"  {key}: {value} ({type(value).__name__})")
    
    return function_components

# ============================================================================
# STEP 3: SAVING PROCESS WITH EXACT PARAMETERS
# ============================================================================

def save_function_with_parameters():
    """
    Shows the exact process and parameters for saving a function
    """
    
    print("\n=== SAVING FUNCTION STEP BY STEP ===")
    
    # Step 1: Get function components
    function_data = show_function_components()
    
    # Step 2: Convert to JSON (required for database storage)
    print("\n--- JSON Conversion ---")
    print("BEFORE (Python Dictionary):")
    print(function_data)
    
    json_string = json.dumps(function_data, indent=2)  # indent=2 makes it readable
    print(f"\nAFTER (JSON String):")
    print(f"Length: {len(json_string)} characters")
    print(f"Type: {type(json_string)}")
    print(f"Content preview: {json_string[:100]}...")
    
    # Step 3: Save to database
    print("\n--- Database Insertion ---")
    connection = sqlite3.connect("my_functions.db")
    cursor = connection.cursor()
    
    # Parameters for INSERT command:
    insert_parameters = {
        "table_name": "saved_functions",
        "columns": ["function_name", "function_info"],  # Which columns to fill
        "values": [function_data["name"], json_string]   # The actual data
    }
    
    print("Insert Parameters:")
    for key, value in insert_parameters.items():
        print(f"  {key}: {value}")
    
    # Execute the insert
    sql_insert = f"INSERT INTO {insert_parameters['table_name']} ({', '.join(insert_parameters['columns'])}) VALUES (?, ?)"
    print(f"\nSQL Command: {sql_insert}")
    print(f"Values: {insert_parameters['values']}")
    
    cursor.execute(sql_insert, insert_parameters['values'])
    connection.commit()
    
    # Show what was actually saved
    cursor.execute("SELECT * FROM saved_functions WHERE function_name = ?", (function_data["name"],))
    saved_data = cursor.fetchone()
    print(f"\n✓ Saved to database. Row: {saved_data}")
    
    connection.close()

# ============================================================================
# STEP 4: LOADING PROCESS WITH EXACT PARAMETERS  
# ============================================================================

def load_function_with_parameters():
    """
    Shows the exact process and parameters for loading functions
    """
    
    print("\n=== LOADING FUNCTION STEP BY STEP ===")
    
    # Step 1: Connect and query database
    connection = sqlite3.connect("my_functions.db")
    cursor = connection.cursor()
    
    # Parameters for SELECT command:
    select_parameters = {
        "table_name": "saved_functions",
        "columns": ["function_name", "function_info"],  # What columns to get
        "where_clause": None  # None means get all rows
    }
    
    print("Select Parameters:")
    for key, value in select_parameters.items():
        print(f"  {key}: {value}")
    
    # Execute the query
    sql_select = f"SELECT {', '.join(select_parameters['columns'])} FROM {select_parameters['table_name']}"
    print(f"\nSQL Command: {sql_select}")
    
    cursor.execute(sql_select)
    all_functions = cursor.fetchall()
    connection.close()
    
    print(f"Found {len(all_functions)} saved functions")
    
    # Step 2: Process each function
    for i, (function_name, function_json) in enumerate(all_functions, 1):
        print(f"\n--- Processing Function {i}: {function_name} ---")
        
        # Convert JSON back to Python dictionary
        print("JSON to Python conversion:")
        print(f"  Input (JSON): {function_json[:50]}...")
        
        function_data = json.loads(function_json)
        print("  Output (Python Dictionary):")
        for key, value in function_data.items():
            print(f"    {key}: {value}")
        
        # Show how to use the loaded data
        print(f"\n  How to execute this function:")
        print(f"    Action Type: {function_data['action_type']}")
        if function_data['action_type'] == 'move_mouse':
            print(f"    Command: pyautogui.moveTo({function_data['mouse_x']}, {function_data['mouse_y']}, duration={function_data['duration']})")

# ============================================================================
# STEP 5: COMPLETE PARAMETER SUMMARY
# ============================================================================

def show_complete_parameter_summary():
    """
    Summary of ALL parameters needed for the complete system
    """
    
    print("\n" + "="*60)
    print("COMPLETE PARAMETER SUMMARY")
    print("="*60)
    
    parameters_needed = {
        "Database Creation": {
            "database_filename": "my_functions.db",
            "table_name": "saved_functions", 
            "column_definitions": [
                "id INTEGER PRIMARY KEY AUTOINCREMENT",
                "function_name TEXT",
                "function_info TEXT"
            ]
        },
        
        "Function Components": {
            "required_fields": ["name", "action_type"],
            "action_fields": ["mouse_x", "mouse_y", "duration"],
            "display_fields": ["description", "label_text", "label_color"],
            "optional_fields": ["created_at", "execution_count", "is_active"]
        },
        
        "Save Process": {
            "conversion": "json.dumps(function_data)",
            "sql_command": "INSERT INTO saved_functions (function_name, function_info) VALUES (?, ?)",
            "parameters": ["function_name", "json_string"]
        },
        
        "Load Process": {
            "sql_command": "SELECT function_name, function_info FROM saved_functions",
            "conversion": "json.loads(json_string)",
            "execution": "Use function_data dictionary to recreate action"
        }
    }
    
    for category, details in parameters_needed.items():
        print(f"\n{category}:")
        for key, value in details.items():
            if isinstance(value, list):
                print(f"  {key}:")
                for item in value:
                    print(f"    - {item}")
            else:
                print(f"  {key}: {value}")

# ============================================================================
# RUN THE DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    # Run all the steps to show the complete process
    create_database_step_by_step()
    save_function_with_parameters() 
    load_function_with_parameters()
    show_complete_parameter_summary()
    
    print(f"\n{'='*60}")
    print("DEMONSTRATION COMPLETE!")
    print("Check 'my_functions.db' file to see the saved data.")
    print("="*60)
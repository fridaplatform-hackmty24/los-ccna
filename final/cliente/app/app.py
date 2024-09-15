from flask import Flask, jsonify, request, render_template
import time
import mysql.connector

app = Flask(__name__)

# Database connection function (optional, can be removed if not needed)
def get_db_connection():
    return mysql.connector.connect(
        host='sanders.c3coace2uz12.us-east-2.rds.amazonaws.com',
        user='admin',
        password='SandersAdmin123.!',
        database='racks'
    )

@app.route('/racks/<rack_name>/<int:shelves_empty>')
def get_rack_with_empty_shelves(rack_name, shelves_empty):
    try:
        # Construct the alert message
        message = f"Rack {rack_name} has {shelves_empty} empty shelves."

        # Print the message to the console (for debugging purposes)
        print(message)

        # Return a simple JSON response with the alert message
        return jsonify({"message": message}), 200

    except Exception as err:
        return jsonify({"error": str(err)}), 500



@app.route('/db_tables/<rack_name>')
def get_rack(rack_name):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = f"SELECT * FROM {rack_name};"
        cursor.execute(query)
        rack_data = cursor.fetchall()
        conn.close()
        return jsonify({"rack_data": rack_data})
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/db_tables')
def get_num_tables():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'racks';"
        cursor.execute(query)
        tables = cursor.fetchall()
        conn.close()

        table_list = [table[0] for table in tables]
        return jsonify({"tables": table_list})
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error fetching tables: {err}"}), 500

@app.route('/test_db')
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        conn.close()
        return f"Connected to database: {db_name[0]}"
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500

@app.route('/')
def index():
    return render_template('index.html', time=time)

@app.route('/test')
def test():
    return render_template('test.html', time=time)

@app.route('/racks/<rack_name>')
def racks(rack_name):
    return render_template('Racks.html', time=time, rack_name=rack_name)

# Keeping rack_info route if still needed
#@app.route('/rack_info', methods=['POST'])
#def get_rack_info():
 #   try:
  #      data = request.get_json()
#
 #       if data is None:
  #          return jsonify({'error': 'Invalid or missing JSON data'}), 400
#
 #       rack_num = data.get('rack_num')
  #      empty_shelves = data.get('empty_shelves')
#
 #       if rack_num is None or empty_shelves is None:
  #          return jsonify({'error': 'Missing rack_num or empty_shelves'}), 400
#
 #       return jsonify({
  #          'message': 'Rack info received',
   #         'rack_num': rack_num,
    #        'empty_shelves': empty_shelves
     #   }), 200
    #except mysql.connector.Error as e:
     #   return jsonify({'error': str(e)}), 500
#Replacing the rack_alert endpoint with alert
# @app.route('/alert', methods=['GET'])
# def alert():
#     try:
#         data = request.get_json()

#         # Check if data is provided and valid
#         if data is None:
#             return jsonify({'error': 'Invalid or missing JSON data'}), 400

#         rack_num = data.get('rack_num')
#         empty_shelves = data.get('empty_shelves')

#         # Check if the required fields are present
#         if rack_num is None or empty_shelves is None:
#             return jsonify({'error': 'Missing rack_num or empty_shelves'}), 400

#         # Example condition to trigger an alert
#         if empty_shelves > 5:
#             alert_message = f"Rack {rack_num} has more than 5 empty shelves!"
#             return jsonify({'alert': alert_message}), 200

#         return jsonify({
#             'message': 'Rack info received',
#             'rack_num': rack_num,
#             'empty_shelves': empty_shelves
#         }), 200

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# Other existing routes
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

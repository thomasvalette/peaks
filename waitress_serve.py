from waitress import serve
import peaks
serve(peaks.app, host='0.0.0.0', port=80)

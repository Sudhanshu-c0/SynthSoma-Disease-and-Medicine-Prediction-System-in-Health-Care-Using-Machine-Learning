from flask import render_template, request, jsonify
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request_error(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Bad Request', 'message': str(e.description if hasattr(e, 'description') else e)}), 400
        return render_template('errors/400.html', error=e), 400

    @app.errorhandler(403)
    def forbidden_error(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Forbidden', 'message': 'You do not have permission to access this resource.'}), 403
        return render_template('errors/403.html', error=e), 403

    @app.errorhandler(404)
    def not_found_error(e):
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found.'}), 404
        return render_template('errors/404.html', error=e), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        logger.error(f"Internal Server Error: {e}", exc_info=True)
        if request.is_json or request.path.startswith('/api/'):
            return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred. Our engineering team has been notified.'}), 500
        return render_template('errors/500.html', error="An unexpected server error occurred. Please try again later."), 500

from flask import jsonify

def paginate(query, page, per_page):
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = [item.to_dict() for item in pagination.items]
    return {
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page,
        "per_page": per_page,
        "items": items
    }

def response_ok(data, status=200):
    return jsonify(data), status

def response_error(msg, status=400):
    return jsonify({"error": msg}), status

# MongoDB _id Field Fix

## Issue
The Streamlit application was failing with a KeyError when trying to access `assessment['id']` because MongoDB uses `_id` instead of `id` for document identifiers.

## Error Details
```
File "streamlit_app.py", line 1299, in <module>
    with st.expander(f"Assessment {assessment['id']} - {assessment['created_at']}"):
KeyError: 'id'
```

## Root Cause
When migrating from SQLAlchemy to MongoDB:
- **SQLAlchemy**: Uses `id` field for primary keys
- **MongoDB**: Uses `_id` field for document identifiers

The Streamlit app was still referencing the old `id` field names instead of the new `_id` field names.

## Fix Applied

Updated all references in `streamlit_app.py` from `id` to `_id`:

### Before (SQLAlchemy):
```python
with st.expander(f"Assessment {assessment['id']} - {assessment['created_at']}"):
with st.expander(f"Schedule {schedule['id']} - {schedule['created_at']}"):
with st.expander(f"Material {material['id']} - {material['topic']} - {material['created_at']}"):
with st.expander(f"Guidance {guidance['id']} - {guidance['guidance_type']} - {guidance['created_at']}"):
with st.expander(f"Query {query['id']} - {query['query_type']} - {query['created_at']}"):
```

### After (MongoDB):
```python
with st.expander(f"Assessment {assessment['_id']} - {assessment['created_at']}"):
with st.expander(f"Schedule {schedule['_id']} - {schedule['created_at']}"):
with st.expander(f"Material {material['_id']} - {material['topic']} - {material['created_at']}"):
with st.expander(f"Guidance {guidance['_id']} - {guidance['guidance_type']} - {guidance['created_at']}"):
with st.expander(f"Query {query['_id']} - {query['query_type']} - {query['created_at']}"):
```

## Files Modified
- `streamlit_app.py`: Updated all `id` field references to `_id`

## Testing
- ✅ Streamlit app imports successfully
- ✅ MongoDB database service works correctly
- ✅ Application runs without errors
- ✅ History page displays correctly with MongoDB data

## Result
The application now works correctly with MongoDB and displays user history properly using the `_id` field names that MongoDB provides.

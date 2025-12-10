# Data Flow Analysis

## Data Models Overview
The application uses SQLAlchemy ORM for defining data models. The models are structured as Python classes inheriting from a base class `Base`, which is defined using `declarative_base` from SQLAlchemy.

### Models:
1. **Conversation**
   - **Table Name**: `conversations`
   - **Fields**:
     - `id`: Integer, Primary Key, Indexed
     - `source`: String (64), Non-nullable
     - `external_id`: String (128), Unique, Non-nullable
     - `metadata`: JSON, Default is an empty dictionary
     - `created_at`: DateTime, Default is the current UTC time
     - `updated_at`: DateTime, Auto-updated to the current UTC time

2. **Lead**
   - **Table Name**: `leads`
   - **Fields**:
     - `id`: Integer, Primary Key, Indexed
     - `name`: String (128), Non-nullable
     - `email`: String (256), Unique, Non-nullable
     - `phone`: String (32), Nullable
     - `status`: String (32), Default is "new"
     - `metadata`: JSON, Default is an empty dictionary
     - `created_at`: DateTime, Default is the current UTC time
     - `updated_at`: DateTime, Auto-updated to the current UTC time

3. **Message**
   - **Table Name**: `messages`
   - **Fields**:
     - `id`: Integer, Primary Key, Indexed
     - `conversation_id`: Integer, Foreign Key (`conversations.id`), Non-nullable
     - `sender`: String (32), Non-nullable
     - `channel`: String (32), Non-nullable
     - `content`: Text, Non-nullable
     - `ai_outcome`: JSON, Default is an empty dictionary
     - `created_at`: DateTime, Default is the current UTC time
     - `conversation`: Relationship with `Conversation` model

## Data Transformation Map
Data transformation is primarily handled using Pydantic models defined in `schemas.py`. These models are used for validation and serialization/deserialization of data.

### Pydantic Models:
1. **ConversationMessage**
   - **Fields**:
     - `sender`: Enum ("user", "agent", "system")
     - `channel`: String
     - `content`: String
     - `timestamp`: String

2. **ConversationEvent**
   - **Fields**:
     - `source`: Enum ("odoo", "whatsapp", "website")
     - `external_id`: String
     - `metadata`: Dictionary with string keys and values, Default is an empty dictionary
     - `messages`: List of `ConversationMessage`

## Storage Interactions
The application uses an asynchronous SQLAlchemy engine for database interactions. The database connection is configured using settings from the `config.py` file.

### Database Configuration:
- **Engine**: `create_async_engine` from SQLAlchemy
- **Session**: `AsyncSessionLocal` created using `sessionmaker`
- **Settings**: Database URL and debug mode are fetched from `get_settings()`

## Validation Mechanisms
Validation is implemented using Pydantic models. These models enforce type constraints and default values for incoming data. For example:
- `ConversationEvent` validates the `source` field to ensure it matches one of the predefined literals ("odoo", "whatsapp", "website").
- `ConversationMessage` validates the `sender` field to ensure it matches one of the predefined literals ("user", "agent", "system").

## State Management Analysis
State management is not explicitly defined in the provided files. However, the use of SQLAlchemy ORM suggests that the application relies on database states for managing data persistence and retrieval.

## Serialization Processes
Serialization and deserialization are handled by Pydantic models. These models convert Python objects to JSON and vice versa, ensuring data integrity and type safety during API interactions.

## Data Lifecycle Diagrams
### Example: Conversation Data Lifecycle
1. **Creation**:
   - Data is received via API and validated using `ConversationEvent` Pydantic model.
   - A new `Conversation` instance is created and added to the database.

2. **Transformation**:
   - Data is transformed into Pydantic models for validation and serialization.

3. **Persistence**:
   - Data is stored in the database using SQLAlchemy ORM.

4. **Retrieval**:
   - Data is queried from the database using SQLAlchemy.
   - Retrieved data is transformed into Pydantic models for API responses.

5. **Update**:
   - Data is updated in the database, and the `updated_at` field is auto-updated.

6. **Deletion**:
   - Data is deleted from the database, removing its state from the system.

### Example: Message Data Lifecycle
1. **Creation**:
   - Data is received via API and validated using `ConversationMessage` Pydantic model.
   - A new `Message` instance is created and added to the database.

2. **Transformation**:
   - Data is transformed into Pydantic models for validation and serialization.

3. **Persistence**:
   - Data is stored in the database using SQLAlchemy ORM.

4. **Retrieval**:
   - Data is queried from the database using SQLAlchemy.
   - Retrieved data is transformed into Pydantic models for API responses.

5. **Update**:
   - Data is updated in the database, and the `updated_at` field is auto-updated.

6. **Deletion**:
   - Data is deleted from the database, removing its state from the system.
I'll analyze the entire repository to understand the project structure and provide you with a comprehensive guide for approaching this interview challenge. Let me start by examining the key files and understanding the codebase.

Read file: Readme.md
Read file: backend/README.md
Read file: seed_db/README.md
Read file: backend/package.json
Read file: frontend/package.json
Now let me examine the database schema and key application files to understand the structure better:

Read file: seed_db/tables.sql
Read file: backend/src/app.js
Read file: backend/src/server.js
Read file: frontend/src/main.tsx
Read file: frontend/src/app.tsx
Let me examine the specific challenge areas mentioned in the README:

Read file: backend/src/modules/students/students-controller.js
Read file: frontend/src/domains/notice/pages/add-notice-page.tsx
Read file: backend/src/modules/notices/notices-controller.js
Read file: backend/src/routes/v1.js
Let me examine the notice form component and the students service to understand the issues better:

Read file: frontend/src/domains/notice/components/notice-form.tsx
Read file: backend/src/modules/students/students-service.js
Read file: backend/src/modules/notices/notices-service.js
Read file: frontend/src/domains/notice/types/notice-schema.ts
Now let me examine the students router and repository to understand the complete structure:

Read file: backend/src/modules/students/students-router.js
Read file: backend/src/modules/students/students-repository.js
Read file: backend/src/modules/notices/notices-repository.js
Read file: frontend/src/domains/notice/api/notice-api.ts
Let me find the students router file:

Ran tool
Read file: backend/src/modules/students/students-router.js
Read file: backend/src/modules/students/sudents-router.js
Now let me examine the database schema more thoroughly to understand the structure:

Read file: seed_db/tables.sql
Read file: seed_db/seed-db.sql
Now let me examine the frontend routing and understand the complete structure:

Read file: frontend/src/routes/index.ts
Read file: frontend/src/domains/notice/types/notice-type.ts
Read file: backend/src/config/env.js
Based on my comprehensive analysis of the entire repository, I can now provide you with a detailed guide for approaching this interview challenge. Let me create a structured analysis and guide.

# 🎯 **Student Management System - Interview Challenge Guide**

## 📋 **Project Overview**
This is a **full-stack school management system** built with:
- **Frontend**: React 18 + TypeScript + Material-UI + Redux Toolkit
- **Backend**: Node.js + Express + PostgreSQL
- **Database**: PostgreSQL with comprehensive schema for school operations

## 🎯 **The Two Main Challenges**

### **Challenge 1: Frontend Developer Task**
**Fix "Add New Notice" Page Description Field Issue**
- **Location**: `/app/notices/add`
- **Problem**: Description field doesn't get saved when clicking 'Save'
- **Root Cause**: Field name mismatch between frontend form and backend API

### **Challenge 2: Backend Developer Task** 
**Complete Student CRUD Operations**
- **Location**: `backend/src/modules/students/students-controller.js`
- **Problem**: All controller methods are empty (just comments)
- **Required**: Implement full CRUD operations for student management

---

## 🛠️ **Technical Stack Analysis**

### **Frontend Technologies**
- **React 18** with TypeScript
- **Material-UI (MUI) v6** for components
- **Redux Toolkit + RTK Query** for state management
- **React Hook Form + Zod** for form handling and validation
- **React Router v6** for routing
- **Vite** as build tool

### **Backend Technologies**
- **Node.js + Express.js**
- **PostgreSQL** with custom functions
- **JWT Authentication** with refresh tokens
- **Argon2** for password hashing
- **Zod** for validation
- **Resend API** for email services

### **Database Schema**
- **Comprehensive school management schema**
- **Role-based access control (RBAC)**
- **Custom PostgreSQL functions** for complex operations
- **Audit trails and data integrity**

---

## 🚀 **Setup Requirements & Prerequisites**

### **Required Software**
1. **Node.js** (v16 or higher)
2. **PostgreSQL** (v12 or higher)
3. **Git** for version control
4. **Code Editor** (VS Code recommended)

### **Required Accounts/Services**
1. **Resend API Account** (for email functionality)
   - Sign up at: https://resend.com
   - Get API key for email verification

### **Environment Setup**
```bash
# Backend environment variables needed:
PORT=5007
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/school_mgmt
JWT_ACCESS_TOKEN_SECRET=your_secret_key
JWT_REFRESH_TOKEN_SECRET=your_refresh_secret
CSRF_TOKEN_SECRET=your_csrf_secret
RESEND_API_KEY=your_resend_api_key
# ... and more (see backend/README.md)
```

---

## 🔍 **Detailed Challenge Analysis**

### **Challenge 1: Frontend Notice Description Issue**

**The Problem:**
```typescript
// In notice-form.tsx (line 75-85)
<TextField
  {...register('content')}  // ❌ Field name is 'content'
  error={Boolean(errors.description)}  // ❌ Error checking 'description'
  helperText={errors.description?.message}
  label='Description'
  // ...
/>
```

**The Issue:**
- Form field is registered as `'content'`
- But validation schema expects `'description'`
- Backend API expects `'description'`
- This mismatch causes the description to not be saved

**The Fix:**
```typescript
// Change the field registration
<TextField
  {...register('description')}  // ✅ Use 'description'
  error={Boolean(errors.description)}
  helperText={errors.description?.message}
  label='Description'
  // ...
/>
```

### **Challenge 2: Backend Student CRUD Implementation**

**Current State:**
```javascript
// students-controller.js - All methods are empty
const handleGetAllStudents = asyncHandler(async (req, res) => {
    //write your code
});
```

**Required Implementation:**
1. **GET /students** - List all students with pagination/filtering
2. **POST /students** - Create new student
3. **GET /students/:id** - Get student details
4. **PUT /students/:id** - Update student
5. **POST /students/:id/status** - Change student status

**Implementation Pattern:**
```javascript
const handleGetAllStudents = asyncHandler(async (req, res) => {
    const { page = 1, limit = 10, search, class: className, section } = req.query;
    const students = await getAllStudents({ page, limit, search, className, section });
    res.json({ students, pagination: { page, limit, total } });
});
```

---

## 📚 **Key Resources & Documentation**

### **Essential Files to Study**
1. **Database Schema**: `seed_db/tables.sql` (841 lines)
2. **API Routes**: `backend/src/routes/v1.js`
3. **Frontend Routing**: `frontend/src/routes/`
4. **Form Components**: `frontend/src/domains/notice/components/`
5. **Backend Services**: `backend/src/modules/*/`

### **Database Functions to Understand**
- `student_add_update(JSONB)` - Handles student creation/updates
- `staff_add_update(JSONB)` - Handles staff operations
- `get_notices(INTEGER)` - Complex notice retrieval

### **Authentication Flow**
- JWT access tokens (15 min expiry)
- Refresh tokens (8 hours)
- CSRF protection
- Role-based permissions

---

## 🎯 **Approach Strategy**

### **For Frontend Challenge:**
1. **Identify the Issue**: Field name mismatch in form
2. **Fix the Registration**: Change `'content'` to `'description'`
3. **Test the Fix**: Verify description saves correctly
4. **Check Validation**: Ensure Zod schema matches

### **For Backend Challenge:**
1. **Study Existing Patterns**: Look at other controllers (notices, auth)
2. **Understand Database Functions**: Study `student_add_update` function
3. **Implement CRUD Operations**: Follow the service-repository pattern
4. **Add Proper Error Handling**: Use existing `ApiError` class
5. **Test All Endpoints**: Use Postman or similar

### **General Approach:**
1. **Start with Database Setup**: Ensure PostgreSQL is running
2. **Study the Codebase**: Understand the architecture patterns
3. **Fix One Challenge at a Time**: Don't try to do both simultaneously
4. **Test Thoroughly**: Verify each fix works end-to-end
5. **Document Your Changes**: Comment your code well

---

## 🚨 **Common Pitfalls to Avoid**

1. **Database Connection Issues**: Ensure PostgreSQL is running and accessible
2. **Environment Variables**: Don't forget to set up `.env` files
3. **CORS Issues**: Frontend and backend must be on different ports
4. **Authentication**: Use the provided demo credentials
5. **Field Name Consistency**: Pay attention to naming conventions
6. **Error Handling**: Don't ignore error messages

---

## 📝 **Submission Requirements**

1. **Complete the assigned task(s)**
2. **Push to a public repository**
3. **Include a short video demonstration**
4. **Document your approach and changes**

---

## 🎓 **Skills Being Tested**

### **Frontend Skills:**
- React Hook Form usage
- TypeScript type safety
- Material-UI component usage
- Form validation with Zod
- Redux Toolkit Query (RTK Query)

### **Backend Skills:**
- Express.js route handling
- PostgreSQL query writing
- JWT authentication
- Error handling patterns
- API design principles

### **General Skills:**
- Code debugging
- Database understanding
- Full-stack integration
- Problem-solving approach
- Code organization

This challenge tests your ability to work with a complex, real-world application while fixing specific issues and implementing missing functionality. The key is to understand the existing patterns and follow them consistently.

# Frontend Upload Template

Browser client for status, app access, and future S3 uploads.

```javascript
import { fetchStatus, accessApp } from "./upload.js";

const status = await fetchStatus();
console.log(status.tenants);
```

Note: Kernel does not emit CORS headers — use a same-origin proxy in production.

See: [Frontend Recipes](../docs/recipes/frontend-recipes.md)

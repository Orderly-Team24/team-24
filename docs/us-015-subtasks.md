# US-015-4: E2E Verification

## Manual Test

1. Get a dish recommendation.
2. Click **I'll order it**.
3. Open **History**.
4. Click **Dislike**.
5. Request another recommendation.
6. Verify the disliked dish is not recommended again.

**Result:** Passed

---

## API

### POST /history/orders/{dish_id}/dislike

Marks a dish as disliked.

```bash
curl -X POST https://team-24.onrender.com/history/orders/123/dislike \
  -H "X-User-Id: user_123"
```

### GET /history/dislikes

Returns the user's disliked dish IDs.

```bash
curl https://team-24.onrender.com/history/dislikes \
  -H "X-User-Id: user_123"
```

---

## Screenshot
![History page showing "Disliked" state.](images/history.jpg)

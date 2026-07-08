import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
const API_RECOMMENDER = 'https://team-24.onrender.com';

function getUserId() {
  return localStorage.getItem("userId") || "";
}

export default function HistoryPage() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pendingDislikes, setPendingDislikes] = useState({});

  useEffect(() => {
    let cancelled = false;

    async function fetchHistory() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_RECOMMENDER}/history/orders`, {
          method: "GET",
          headers: {
            "X-User-Id": getUserId(),
          },
        });

        if (res.ok == false) {
          throw new Error(`Request failed with status ${res.status}`);
        }

        const data = await res.json();
        if (!cancelled) {
          setOrders(data.orders || []);
        }
      } catch (err) {
        if (!cancelled) {
          setError(
            "Couldn't load your order history. Please try again in a moment."
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    fetchHistory();

    return () => {
      cancelled = true;
    };
  }, []);

  async function handleDislike(dishId) {
    setPendingDislikes((prev) => ({ ...prev, [dishId]: true }));

    try {
      const res = await fetch(
        `${API_RECOMMENDER}/history/orders/${dishId}/dislike`,
        {
          method: "POST",
          headers: {
            "X-User-Id": getUserId(),
          },
        }
      );

      if (!res.ok) {
        throw new Error(`Request failed with status ${res.status}`);
      }

      setOrders((prev) =>
        prev.map((order) =>
          order.dish_id === dishId ? { ...order, disliked: true } : order
        )
      );
    } catch (err) {
      setOrders((prev) =>
        prev.map((order) =>
          order.dish_id === dishId
            ? { ...order, dislikeError: true }
            : order
        )
      );
    } finally {
      setPendingDislikes((prev) => {
        const next = { ...prev };
        delete next[dishId];
        return next;
      });
    }
  }

  if (loading) {
    return (
      <div className="history-page">
        <h1>Order History</h1>
        <p>Loading your order history…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="history-page">
        <h1>Order History</h1>
        <p className="error-message">{error}</p>
      </div>
    );
  }

  return (
    <div className="history-page">
      <h1>Order History</h1>

      {orders.length === 0 ? (
        <p>You haven't ordered anything yet.</p>
      ) : (
        <div className="history-list">
          {orders.map((order) => {
            const isPending = !!pendingDislikes[order.dish_id];
            return (
              <div
                key={order.dish_id}
                className={`history-card${order.disliked ? " disliked" : ""}`}
              >
                <div className="history-card-info">
                  <h3>{order.name}</h3>
                  {order.price != null && <p>${order.price.toFixed(2)}</p>}
                  {order.ordered_at && (
                    <p className="ordered-at">
                      Ordered on {new Date(order.ordered_at).toLocaleDateString()}
                    </p>
                  )}
                  {order.dislikeError && (
                    <p className="error-message small">
                      Couldn't save — try again.
                    </p>
                  )}
                </div>

                <button
                  className="dislike-button"
                  disabled={order.disliked || isPending}
                  onClick={() => handleDislike(order.dish_id)}
                >
                  {order.disliked
                    ? "Disliked ✓"
                    : isPending
                    ? "Saving…"
                    : "Dislike"}
                </button>
              </div>
            );
          })}
        </div>
      )}

      <Link to="/food-recommender" className="back-link">
        ← Back
      </Link>
    </div>
  );
}

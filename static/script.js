// Immediately invoked to avoid polluting global scope
const chatbotActivate = () => {
  console.log("🤖 CHATBOT ACTIVATED");

  // DOM elements
  const chatInput = document.querySelector(".chat-input textarea");
  const sendChatBtn = document.querySelector("#send-btn");
  const chatBox = document.querySelector(".chatbox");
  const chatToggle = document.querySelector(".chatbot-toggle");
  const chatbotCloseBtn = document.querySelector("#chatbot-close-btn");
  const chatContainer = document.querySelector("#chatBot");

  let userMessage;
  const inputInitHeight = chatInput.scrollHeight;

  // Create timestamp
  const createRequestTime = () => {
    const date = new Date();
    const day = String(date.getDate()).padStart(2, "0");
    const month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][date.getMonth()];
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");

    const chatLi = document.createElement("li");
    chatLi.classList.add("chat-time");
    chatLi.innerHTML = `<p>${day} ${month} ${hours}:${minutes}</p>`;
    return chatLi;
  };

  // Create a chat bubble
  const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    chatLi.innerHTML = `<p>${message}</p>`;
    return chatLi;
  };

  // Scroll to bottom
  const scrollChatToBottom = () => {
    chatBox.scrollTop = chatBox.scrollHeight;
  };

  // Handle send
  const handleChat = () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) return;

    // Reset input
    chatInput.value = "";
    chatInput.style.height = `${inputInitHeight}px`;

    // Add user message and timestamp
    chatBox.appendChild(createRequestTime());
    chatBox.appendChild(createChatLi(userMessage, "outgoing"));
    scrollChatToBottom();

    // Add loading indicator
    const incomingChatLi = createChatLi("Typing...", "incoming");
    chatBox.appendChild(incomingChatLi);
    scrollChatToBottom();

    generateResponse(incomingChatLi, userMessage);
  };

  // Communicate with Flask API
  const generateResponse = (li, message) => {
    const API_URL = "https://nutribuddy-ai-enabled-meal-planner-npxd.onrender.com"; // replace with deployed endpoint later
    const messageElement = li.querySelector("p");

    fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    })
      .then((res) => res.json())
      .then((data) => {
        messageElement.textContent = data.response || "🤖 No response.";
      })
      .catch((err) => {
        console.error("Chat error:", err);
        messageElement.classList.add("error");
        messageElement.textContent = "❌ Something went wrong. Please try again.";
      })
      .finally(() => {
        scrollChatToBottom();
      });
  };

  // Auto-resize input
  chatInput.addEventListener("input", () => {
    chatInput.style.height = `${inputInitHeight}px`;
    chatInput.style.height = `${chatInput.scrollHeight}px`;
  });

  // Submit on Enter (desktop only)
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey && window.innerWidth > 800) {
      e.preventDefault();
      handleChat();
    }
  });

  // Send button click
  sendChatBtn.addEventListener("click", handleChat);

  // Open chatbot
  chatToggle.addEventListener("click", () => {
    chatContainer.classList.toggle("show-chatbot");
    scrollChatToBottom();
  });

  // Close chatbot
  chatbotCloseBtn.addEventListener("click", () => {
    chatContainer.classList.remove("show-chatbot");
  });

  // Click outside to close
  document.addEventListener("click", (e) => {
    if (!chatContainer.contains(e.target) && !chatToggle.contains(e.target)) {
      chatContainer.classList.remove("show-chatbot");
    }
  });
};

// Activate chatbot
chatbotActivate();

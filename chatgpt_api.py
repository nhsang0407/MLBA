from openai import OpenAI

client = OpenAI()  # Tự động lấy key từ biến môi trường


def chat():
    print("Chat với GPT (gõ 'exit' để thoát)\n")

    # Danh sách tin nhắn để lưu lịch sử hội thoại
    messages = [
        {"role": "system", "content": "Bạn là trợ lý AI thân thiện, luôn trả lời bằng tiếng Việt."}
    ]

    while True:
        # Người dùng nhập câu hỏi
        user_input = input("Bạn:")

        if user_input.lower() == "exit":
            print("Kết thúc hội thoại.")
            break

        # Thêm câu hỏi vào messages
        messages.append({"role": "user", "content": user_input})

        # Gửi yêu cầu đến GPT
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )

        # Lấy câu trả lời
        reply = response.choices[0].message.content
        print("GPT:", reply)

        # Lưu câu trả lời vào lịch sử
        messages.append({"role": "assistant", "content": reply})


if __name__ == "__main__":
    chat()

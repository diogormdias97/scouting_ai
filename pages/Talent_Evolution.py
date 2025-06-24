st.title("🔮 Talent Evolution Predictor")
players_df = pd.read_csv("data/players_data.csv")
selected = st.selectbox("Select a player", players_df["Name"].unique())

if selected:
    player = players_df[players_df["Name"] == selected].iloc[0]
    if st.button("Predict Future Evolution"):
        with st.spinner("Thinking..."):
            evolution = call_openai_future_projection(player)
        st.markdown("## 🧠 AI Projection")
        st.markdown(evolution)

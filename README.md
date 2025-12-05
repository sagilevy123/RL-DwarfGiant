# Projectile Interception RL Environment

### Project Description
> [!NOTE]
> **Hyperparameters:** The quantities mentioned below (3 rocks, 3 ball sources, 10 time steps) are fully configurable hyperparameters and can be adjusted in the `consts.py` file.
**The Game Rules:**
1. **Defensive Units (Rocks):** The player controls 3 rocks. Each rock has a **firing cooldown** of 10 time steps.
2. **Threats (Balls):** Incoming balls originate from **3 fixed sources** on the right side. Each source has a unique fixed distribution that dictates its launch frequency and launch angle.

**The Goal:**
To train a Reinforcement Learning (RL) agent that simultaneously discovers the **optimal static positioning** for the rocks and learns the **best firing timing** to maximize interception rates.

**The Method:**
1. **Unified Action Space:** The problem is modeled as a single RL environment where the agent makes two types of decisions:
    * **Placement (Episode Start):** At the beginning of each episode, the agent selects the vertical positions ($Y$ coordinates) for the 3 rocks.
    * **Interception (Real-time):** During the episode, the agent observes the incoming balls and decides when to trigger each rock (subject to cooldown constraints).
2. **Optimization:** Through the reward signal (received for successful hits), the model converges on the optimal layout that provides the best coverage against the specific threat patterns, without needing an external loop for position guessing.
# Author : velan
# Date : Sat-April 8:19 in 2026
# Description : to made a brain neuro connection to make machine think

# Process - Structure :
#  1. Brain -> hold( bunch of neuron and connect it by proper measurements)
#  2. neuron -> hold( content, importance, synapses)

# Terms need to know for work with it
#  1. content -> is a data that hold a infomation
#  2. synapses -> list of sync other neuron
#  3. Algorithm -> (Jaccard-Simularity) is used for to measure the relation of data to sync neuron and make connection with it


# BACKGROUND PROCESS WHAT HAPPEN:
#
# --! BRAIN is OBJECT (MAIN PART) -> that hold bunch of neuron
#    1. learn ->  every piece of information that we give insert as new neuron and  (Sync with related neuron)
#    2. perform -> what it can do [ relate_similarity of info and Sync neuron]
#    3. analyze -> process given query() by
#                       1. finding BEST_ENTRY_POINT( best_neuron : neuron(object) ) in bunch of nueron by techquine of (qeury > similar to > neuro_data)
#                       2. provide related resultby accessing info of " best_neuron.synapses " list


import pickle
import spacy
import os

lol = 4

try:
    nlp = spacy.load("en_core_web_md")
except:
    # If the model isn't downloaded, this prevents a crash
    print("Error: Run 'python3 -m spacy download en_core_web_md' in terminal first.")


def run(cmd: str):
    os.system(cmd)


class neuron:
    # represent a single brain neuron cell holding one piece of information.

    def __init__(self, content):
        self.content = content
        self.synapses = {}  # synapses Link wiht other Neuron object { Neuron : strenght_weight}

    def connect(self, other_neuron, weight):
        self.synapses[other_neuron] = weight


class brain:
    # Brain which is manager that handle syncing and analysis of neurons.

    def __init__(self, sensitivity: float = 0.2):
        self.network = []
        self.sensitivity = sensitivity  # how related data must be to sync

    def _calculate_similarity(self, str1: str, str2: str):
        # Calculate commonality between two data strings.
        #   JACCARD-Simularity Algorithm used here to analaysis this check "https://www.geeksforgeeks.org/python/jaccard-similarity/"
        #
        #   return weight(matching percentange)

        # Optimise String for analaysis
        s1 = set(str1.lower().split())
        s2 = set(str2.lower().split())

        # Apply on Formula
        intersection = len(s1.intersection(s2))
        union = len(s1.union(s2))

        # return Value
        return intersection / union if union > 0 else 0

    def learn(self, info):
        # Create a neuron and automatically syncs it with related ones.
        new_node = neuron(info)

        for exist_neuron in self.network:
            # Make Weight(score) by depend on Similarity
            score = self._calculate_similarity(info, exist_neuron.content)
            if score >= self.sensitivity:
                # Syncing : connect them bidirectionally
                new_node.connect(exist_neuron, score)
                exist_neuron.connect(new_node, score)

        self.network.append(new_node)
        print(f"Learned : '{info}' (Synced with {len(new_node.synapses)} other)")

    def analyze(self, query):
        """
        Analyzes query and synthesizes a thematic summary rather than a list.
        """
        query_doc = nlp(query)

        # 1. Activation: Find the entry point
        best_neuron = None
        max_relevance = 0

        for n in self.network:  # Note: Ensure your init uses self.network
            neuron_doc = nlp(n.content)
            score = query_doc.similarity(neuron_doc)
            if score > max_relevance:
                max_relevance = score
                best_neuron = n

        if not best_neuron or max_relevance < 0.3:
            return "Neural pathways are too weak to form a conclusion."

        # 2. Thematic Extraction: Gather the cluster
        cluster_docs = [nlp(best_neuron.content)]
        for neighbor in best_neuron.synapses:
            cluster_docs.append(nlp(neighbor.content))

        # 3. Intelligence Logic: Find common Nouns and Adjectives (The 'Theme')
        all_keywords = []
        for doc in cluster_docs:
            # Extract only the 'meat' of the sentence
            keywords = [
                token.lemma_.lower()
                for token in doc
                if token.pos_ in ["NOUN", "ADJ"] and not token.is_stop
            ]
            all_keywords.extend(keywords)

        from collections import Counter

        common_themes = [word for word, count in Counter(all_keywords).most_common(3)]
        theme_str = " & ".join(common_themes).upper()

        # 4. Final Summarized Output
        # Instead of 'A + B', we describe the relationship
        summary = (
            f"IDENTIFIED THEME: [{theme_str}]\n"
            f"CORE KNOWLEDGE:  '{query}' with {best_neuron.content}. "
        )

        return summary

    def ask(self, query: str):
        print("\n--- QUERY RESULT ---")
        result = self.analyze(query)
        print(f"Brain Summary: {result}")

    def save_network(self, filename="brain_network.pkl"):
        # Save tranind neuron as file
        with open(filename, "wb") as file:
            pickle.dump(self.network, file)
        print(f"✔️ Brain state saved to {filename}")

    def load_network(self, filename="brain_network.pkl"):
        # Load trained neurons from file
        if os.path.exists(filename):
            with open(filename, "rb") as file:
                self.network = pickle.load(file)
            print(f"🧠 Brain state restored. {len(self.network)} neurons loaded.")
        else:
            print("⚠️ No saved brain found. Starting fresh.")


Brain = brain()

import pandas as pd
import networkx as nx

# Load the psxhax pages data from CSV
pages_info_df = pd.read_csv('psxhax_pages_info.csv')
# Create a directed graph
G = nx.DiGraph()

# Add nodes to the graph
for index, row in pages_info_df.iterrows():
    src_page_id = row['page_id']
    G.add_node(src_page_id)
print('Calculating PageRank values please wait ...')
for index, row in pages_info_df.iterrows():
    src_page_id = row['page_id']
    # Check if there are links in links column
    links = row['links']
    if pd.notna(links):
        links = row['links'].split(',')
        for link in links:
            # Search for dest_page id
            matching_row = pages_info_df.loc[pages_info_df['page_url'] == link]
            if not matching_row.empty:
                dest_page_id = matching_row.index[0]
                G.add_edge(src_page_id, dest_page_id)

# Run the PageRank algorithm
pagerank_scores = nx.pagerank(G, max_iter=50, alpha=0.85)

# Assign the PageRank scores to the psxhax pages dataframe
pages_info_df['page_rank'] = [pagerank_scores[page_id] for page_id in pages_info_df['page_id']]

# Sort the psxhax pages based on PageRank scores
ranked_pages_df = pages_info_df.sort_values(by=['page_rank', 'page_id'], ascending=[False, True])

# Save the ranked psxhax pages information to CSV
ranked_pages_df.to_csv('ranked_psxhax_pages.csv', index=False)
print('\n')
print('==========================================================')
print('\nPsxhax pages ranks saved to ranked_psxhax_pages.csv successfully.')

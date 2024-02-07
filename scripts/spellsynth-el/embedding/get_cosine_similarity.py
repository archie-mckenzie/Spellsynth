from typing import List
import numpy as np

def get_cosine_similarity(alpha: List[float], beta: List[float]):
    alpha_np = np.array(alpha)
    beta_np = np.array(beta)
    dot_product = np.dot(alpha_np, beta_np)
    norm_alpha = np.linalg.norm(alpha_np)
    norm_beta = np.linalg.norm(beta_np)
    return dot_product / (norm_alpha * norm_beta)

import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Hàm tạo ma trận khoảng cách ngẫu nhiên giữa các thành phố
def create_distance_matrix(num_cities):
    distance_matrix = []
    for i in range(num_cities):
        row = []
        for j in range(num_cities):
            if i == j:
                row.append(0)  # Khoảng cách giữa một thành phố với chính nó là 0
            elif j > i:
                row.append(random.randint(1, 300))  # Khoảng cách ngẫu nhiên giữa hai thành phố
            else:
                row.append(distance_matrix[j][i])  # Đối xứng khoảng cách (i->j = j->i)
        distance_matrix.append(row)
    return distance_matrix

# Hàm tạo giải pháp ban đầu ngẫu nhiên
def generate_random_solution(num_cities):
    cities = list(range(num_cities))  # Danh sách các thành phố
    solution = []
    for i in range(num_cities):
        random_city = random.choice(cities)  # Chọn ngẫu nhiên một thành phố
        solution.append(random_city)  # Thêm thành phố vào giải pháp
        cities.remove(random_city)  # Loại thành phố đó khỏi danh sách
    return solution

# Hàm tính độ dài tổng quãng đường của một giải pháp
def calculate_route_length(tsp, solution):
    total_length = 0
    segments = []  # Danh sách các đoạn đường
    for i in range(len(solution)):
        start = solution[i - 1]  # Thành phố bắt đầu
        end = solution[i]  # Thành phố kết thúc
        distance = tsp[start][end]  # Khoảng cách giữa hai thành phố
        segments.append((start, end, distance))  # Lưu thông tin đoạn đường
        total_length += distance  # Cộng dồn tổng quãng đường
    return total_length, segments

# Hàm tạo danh sách các giải pháp hàng xóm
def generate_neighbors(solution):
    neighbors = []
    for i in range(len(solution)):
        for j in range(i + 1, len(solution)):
            neighbor = solution.copy()  # Sao chép giải pháp hiện tại
            neighbor[i] = solution[j]  # Hoán đổi vị trí hai thành phố
            neighbor[j] = solution[i]
            neighbors.append(neighbor)  # Thêm giải pháp hàng xóm vào danh sách
    return neighbors

# Hàm tìm giải pháp hàng xóm tốt nhất
def find_best_neighbor(tsp, neighbors):
    best_length, best_segments = calculate_route_length(tsp, neighbors[0])  # Độ dài của hàng xóm đầu tiên
    best_neighbor = neighbors[0]  # Gán hàng xóm đầu tiên làm tốt nhất ban đầu
    for neighbor in neighbors:
        current_length, _ = calculate_route_length(tsp, neighbor)  # Tính độ dài hàng xóm hiện tại
        if current_length < best_length:  # Nếu hàng xóm hiện tại tốt hơn
            best_length = current_length
            best_neighbor = neighbor
    return best_neighbor, best_length

# Lớp Hill Climbing giải bài toán Người du lịch
class HillClimbing:
    def __init__(self, num_cities):
        self.matrix = None  # Ma trận khoảng cách
        self.result = None  # Kết quả giải thuật
        self.num_cities = num_cities  # Số lượng thành phố
    
    # Hàm vẽ đồ thị bằng Matplotlib
    def create_plot(self):
        print((self.matrix))
        distance = np.array(self.matrix)
        graph = nx.from_numpy_array(distance)  # Tạo đồ thị từ ma trận
        print(graph)
        positions = nx.spring_layout(graph)  # Tính toán vị trí các nút
        # Vẽ các thành phố và các cạnh
        nx.draw_networkx_nodes(graph, positions, node_color='r')  # Vẽ các thành phố (nút)
        nx.draw_networkx_edges(graph, positions)  # Vẽ các cạnh
        nx.draw_networkx_labels(graph, positions)  # Hiển thị nhãn của các thành phố
        plt.show()  # Hiển thị đồ thị
       
    # Hàm giải bài toán
    def solve(self):
        self.matrix = create_distance_matrix(self.num_cities)  # Tạo ma trận khoảng cách
        current_solution = generate_random_solution(self.num_cities)  # Tạo giải pháp ngẫu nhiên ban đầu
        current_length, segments = calculate_route_length(self.matrix, current_solution)  # Tính tổng độ dài
        
        # Lưu thông tin kết quả
        self.result = "Giải pháp ngẫu nhiên đầu tiên là: " + str([city for city in current_solution]) + "\n"
        self.result += "Độ dài quãng đường ngẫu nhiên đầu tiên là: " + str(current_length) + "\n"
        self.result += "   Chi tiết từng đoạn đường:\n"
        for segment in segments:
            self.result += f"       {segment[0]} -> {segment[1]}: {segment[2]}\n"
        
        neighbors = generate_neighbors(current_solution)  # Tạo các giải pháp hàng xóm
        self.result += "Các giải pháp hàng xóm được tạo ra:\n"
        for neighbor in neighbors:
            neighbor_length, neighbor_segments = calculate_route_length(self.matrix, neighbor)
            self.result += "   " + str([city for city in neighbor]) + " - Độ dài quãng đường hàng xóm này: " + str(neighbor_length) + "\n"
            self.result += "       Chi tiết từng đoạn đường:\n"
            for segment in neighbor_segments:
                self.result += f"           {segment[0]} -> {segment[1]}: {segment[2]}\n"
        
        best_neighbor, best_length = find_best_neighbor(self.matrix, neighbors)  # Tìm hàng xóm tốt nhất
        while best_length < current_length:  # Lặp đến khi không cải thiện được giải pháp
            current_solution = best_neighbor
            current_length, segments = calculate_route_length(self.matrix, current_solution)
            neighbors = generate_neighbors(current_solution)
            best_neighbor, best_length = find_best_neighbor(self.matrix, neighbors)
        
        # Ghi lại giải pháp tốt nhất
        self.result += "Giải pháp tốt nhất: " + str([city for city in current_solution]) + "\n"
        self.result += "Quãng đường ngắn nhất: " + str(current_length) + "\n"
        self.result += "   Chi tiết từng đoạn đường:\n"
        for segment in segments:
            self.result += f"       {segment[0]} -> {segment[1]}: {segment[2]}\n"
        return current_solution

# Hàm chính
def main():
    # Nhập vào số lượng thành phố
    num_cities = int(input("Số lượng thành phố cần đi qua: "))

    if num_cities >= 2:  # Kiểm tra số lượng thành phố hợp lệ
        hill_climbing = HillClimbing(num_cities)  # Tạo đối tượng Hill Climbing
        solution = hill_climbing.solve()  # Giải bài toán
        print(hill_climbing.result)  # In kết quả
        hill_climbing.create_plot()  # Vẽ đồ thị
    else:
        print("Hãy nhập số lượng thành phố >= 2 !!!")  # Cảnh báo nếu số thành phố không hợp lệ

# Chạy chương trình
if __name__ == "__main__":
    main()

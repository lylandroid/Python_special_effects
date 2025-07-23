# 导入Folium库，用于创建交互式地图
import folium

def create_interactive_map(center_location=[39.9042, 116.4074], zoom_start=10, locations=None):
    """
    创建一个交互式地理地图，展示多个地点标记
    参数:
        center_location: 地图中心坐标 [纬度, 经度]，默认是北京
        zoom_start: 初始缩放级别（1-18，越大越近）
        locations: 地点列表，每个地点包含 [名称, 纬度, 经度, 弹出信息]
    """
    # 创建地图对象，以指定坐标为中心
    # 使用OpenStreetMap作为默认底图，视觉效果清晰
    map_obj = folium.Map(location=center_location, zoom_start=zoom_start, tiles='OpenStreetMap')

    # 如果提供了地点列表，添加标记
    if locations:
        for location in locations:
            name, lat, lon, popup = location
            # 添加标记到地图
            # 标记颜色为蓝色，点击显示中文弹出信息
            folium.Marker(
                location=[lat, lon],
                popup=popup,
                tooltip=name,
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(map_obj)

    # 添加Stamen Terrain底图，带上必要的版权信息
    folium.TileLayer(
        tiles='Stamen Terrain',
        name='地形图',
        attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
    ).add_to(map_obj)

    # 添加地图图层控制，允许用户切换地图样式
    folium.LayerControl().add_to(map_obj)

    # 保存地图为HTML文件，可在浏览器中打开
    output_path = 'out/interactive_map.html'
    map_obj.save(output_path)
    print(f"交互式地图已保存为: {output_path}")

    # 返回地图对象，以便在Jupyter Notebook中直接显示
    return map_obj

# 示例用法
if __name__ == "__main__":
    # 定义一些示例地点（名称, 纬度, 经度, 弹出信息）
    locations = [
        ['天安门', 39.9042, 116.4074, '中国北京的天安门广场，历史文化中心！'],
        ['故宫', 39.9163, 116.3972, '故宫博物院，古代皇宫，文物宝库！'],
        ['长城', 40.4319, 116.5704, '八达岭长城，世界文化遗产！']
    ]

    # 调用函数创建交互式地图，以北京为中心
    create_interactive_map(
        center_location=[39.9042, 116.4074],  # 北京坐标
        zoom_start=10,                        # 初始缩放级别
        locations=locations                   # 地点列表
    )
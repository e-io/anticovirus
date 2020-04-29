import pkg_resources


def version_info(lib):
    version = pkg_resources.get_distribution(lib).version
    return f"{lib}=={version}\n"

if __name__ == "__main__":
    libs = ["vk_api"]

    with open("requirements.txt", 'w') as file:
        for lib in libs:
            file.write(version_info(lib))

    def Move(self):
        direction = [1, -1]
        currentKey = pygame.key.get_pressed()

        if currentKey[pygame.K_w]:
            self.position[1] -= self.speed
            direction = [1, -1]

        if currentKey[pygame.K_a]:
            self.position[0] -= self.speed
            direction = [0, -1]

        if currentKey[pygame.K_s]:
            self.position[1] += self.speed
            direction = [1, 1]

        if currentKey[pygame.K_d]:
            self.position[0] += self.speed
            direction = [0, 1]

        if currentKey[pygame.KMOD_SHIFT]:
            self.position[direction[0]] += direction[1] * 2 * self.speed


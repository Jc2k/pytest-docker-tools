# CHANGELOG



## v0.0.2 (2025-03-14)

### Fix

* fix: version number must be preset ([`46363d2`](https://github.com/Jc2k/pytest-docker-tools/commit/46363d27f84d0bc3c8a968b041c0d5ce729bfdea))

* fix: don&#39;t check in version number ([`1b5adf1`](https://github.com/Jc2k/pytest-docker-tools/commit/1b5adf1411f0a753af5451cec747f5aeda84dfc1))


## v0.0.1 (2025-03-14)

### Chore

* chore: add codespell for ci lint ([`89e5369`](https://github.com/Jc2k/pytest-docker-tools/commit/89e5369c94386fbcc2a81a767b48128e94cfe70f))

### Fix

* fix: get all lints passing ([`7556579`](https://github.com/Jc2k/pytest-docker-tools/commit/7556579ab941837d5b7f76344a7a2dd9bc082ada))

* fix: pre-commit settings ([`f50ebf1`](https://github.com/Jc2k/pytest-docker-tools/commit/f50ebf1d103f85255839fa658ab03403377fe2d8))

* fix: explicit build backend ([`2cb886b`](https://github.com/Jc2k/pytest-docker-tools/commit/2cb886b9b6be481a779005a66033f6c159138fce))

* fix: drop unsupported pythons ([`9310ce2`](https://github.com/Jc2k/pytest-docker-tools/commit/9310ce2b457ab87de5f57b13fb32eb2017c5b262))

* fix: run pre-commit under uv ([`ba17370`](https://github.com/Jc2k/pytest-docker-tools/commit/ba173709ddf50425a8c18933bb8aee46f439e44c))

* fix: add pre-commit deps ([`d48cfa6`](https://github.com/Jc2k/pytest-docker-tools/commit/d48cfa6bec6cb357c26c69a9605062831ced42b2))

* fix: make sure ci runs pytest ([`4ad0141`](https://github.com/Jc2k/pytest-docker-tools/commit/4ad01410ff6f0150706945f37e4d01df63e4fd67))

* fix: setuptools configuration was wrong ([`d4e85dc`](https://github.com/Jc2k/pytest-docker-tools/commit/d4e85dc87b4fcc52eb7e5fc81dc4fa7ec0712653))

* fix: modernize ci ([`b00c4f9`](https://github.com/Jc2k/pytest-docker-tools/commit/b00c4f967f16d868648ffcf9bdd9e2c0468d99ef))

### Unknown

* Create LICENSE ([`5853f9b`](https://github.com/Jc2k/pytest-docker-tools/commit/5853f9b67511d76a3bf0d607f4d730b6bac0b969))


## v3.1.3 (2022-02-17)

### Unknown

* Version bump ([`62935c9`](https://github.com/Jc2k/pytest-docker-tools/commit/62935c9bcf40ccca1d79e4941517b2521006c147))

* Version bump ([`78db66f`](https://github.com/Jc2k/pytest-docker-tools/commit/78db66f77529abbbe93c90abfd6005fbe5fd7acf))

* Merge pull request #41 from jmgilman/issues/40

Updates README network section with better example ([`e51d353`](https://github.com/Jc2k/pytest-docker-tools/commit/e51d353a598c53111e568219906a14cfd3263698))

* Reverts pytest changes and fixes import error in README ([`6f8ea99`](https://github.com/Jc2k/pytest-docker-tools/commit/6f8ea9975f461393034103e40549dfced946bf6e))

* Limits pytest to tests/ subdirectory ([`1b16a04`](https://github.com/Jc2k/pytest-docker-tools/commit/1b16a04e8bd680ceb3d2c237166eebeee4ea515f))

* Bumps versions, sets minimum Python version to 3.7.0, adds TOML extra to coverage ([`2e2774e`](https://github.com/Jc2k/pytest-docker-tools/commit/2e2774ee733d482113f0f10ba416cc2c05e2d866))

* Updates README network section with better example ([`65b8edd`](https://github.com/Jc2k/pytest-docker-tools/commit/65b8edd645462958c5919b77ccb54652b749e680))

* Unpin docker version ([`533f806`](https://github.com/Jc2k/pytest-docker-tools/commit/533f806d62dbb68aa6d1944a29368873c1ea36e2))

* Version bumps ([`c7a18ee`](https://github.com/Jc2k/pytest-docker-tools/commit/c7a18eea487d48dc82c302d1439d12dbdd9c41aa))

* Abort release if something breaks ([`11eecfe`](https://github.com/Jc2k/pytest-docker-tools/commit/11eecfedde9414017e872d386e87a1804d57ca9b))

* Version bump ([`858d47d`](https://github.com/Jc2k/pytest-docker-tools/commit/858d47d7d6b84059f3b181ad6cf8645615541a77))

* Merge pull request #39 from phillipuniverse/pytest-7.0

Allow compatibility with Pytest 7.0 ([`23e5c03`](https://github.com/Jc2k/pytest-docker-tools/commit/23e5c0321baad65f4f941338d6b8272673d827ce))

* Allow compatibility with Pytest 7.0 ([`d4a26ef`](https://github.com/Jc2k/pytest-docker-tools/commit/d4a26ef66f31878e9dd3c35824d8d3b4207ed962))

* Merge pull request #38 from alexanderpetrenz/main

Readme.md: Added section on new non-string fixture features ([`49835f0`](https://github.com/Jc2k/pytest-docker-tools/commit/49835f00acfa64aaf2df1e835e12372b4bd70521))

* Readme.md: Added section

Readme.md now has a section explaining how to reference non string returning fixtures. ([`adf4172`](https://github.com/Jc2k/pytest-docker-tools/commit/adf4172b1266928037d9e8ba0d68c0a02c078410))

* Version bump ([`61a7fbd`](https://github.com/Jc2k/pytest-docker-tools/commit/61a7fbd14fb69b7b9df47fe13cbd95a3cba650f3))

* Merge pull request #37 from alexanderpetrenz/main

Add ability to use non string returning Fixtures in Fixture Factory definitions ([`64f9f7a`](https://github.com/Jc2k/pytest-docker-tools/commit/64f9f7aac71a151565c30e7110dbbc0e572f5284))

* added import of fxtr to pytest_docker_tools/__init__.py, adjusted test ([`4e60e7b`](https://github.com/Jc2k/pytest-docker-tools/commit/4e60e7bfb7212c53916234d36d6b924f3809bc5a))

* added some type hints to templates.py ([`99f0968`](https://github.com/Jc2k/pytest-docker-tools/commit/99f09683c5eeec67d6312224ccf6ff3dbf02668a))

* added type hints to exceptions.py ([`2277d4b`](https://github.com/Jc2k/pytest-docker-tools/commit/2277d4beff5b5a479166a446d0d21510f762136e))

* added type hints to utils.py ([`b66581f`](https://github.com/Jc2k/pytest-docker-tools/commit/b66581fa4152ea6e76ddf2d8854304af9253d96d))

* renamed FixtureRef to _FixtureRef and fixtureref to fxtr. Adjusted tests ([`e2ce02a`](https://github.com/Jc2k/pytest-docker-tools/commit/e2ce02ad83477389f65ef68635a24e58ab484297))

* adjusted condition in templates.py. Added test for using fixtures directly ([`a2d1e63`](https://github.com/Jc2k/pytest-docker-tools/commit/a2d1e630e39c7ff8313cd34e1b47e2048a2b59ab))

* moved fixtureref, adjusted tests ([`c8ed81d`](https://github.com/Jc2k/pytest-docker-tools/commit/c8ed81d404718441083f1dc37e60c2c9acc8d6f0))

* Update conftest.py

removed unused import ([`18d5bce`](https://github.com/Jc2k/pytest-docker-tools/commit/18d5bceaa513b0ac809c75f063546e1fcda9f463))

* clean ups ([`6531000`](https://github.com/Jc2k/pytest-docker-tools/commit/65310005ffdc394f381c4b25a2d78d1ce9b61468))

* added tests for using fixtureref and lambda ([`b2d6727`](https://github.com/Jc2k/pytest-docker-tools/commit/b2d6727817eccb89ce4b91cc8df00d7e841751e1))

* removed obsolete fixture ([`12d167b`](https://github.com/Jc2k/pytest-docker-tools/commit/12d167b908bcdd441dff89bd9b90dfda5c82b408))

* extended conditions of classes FixtureFinder and Renderer in templates.py to identify Fixtures which are wrapped in a FixtureRef instance ([`43ae6e1`](https://github.com/Jc2k/pytest-docker-tools/commit/43ae6e1373a89ff914d95a48a14bb61c0628c130))

* added new wrapper class `FixtureRef` ([`6725256`](https://github.com/Jc2k/pytest-docker-tools/commit/6725256635c712f215e3abeb668f9e614a31db6e))

* Update README.md ([`81d6c44`](https://github.com/Jc2k/pytest-docker-tools/commit/81d6c44ae08eba94a88e969873b809f61b1ae09f))

* Version bump ([`55fcf59`](https://github.com/Jc2k/pytest-docker-tools/commit/55fcf59109d218d054479de29095d31e6e0bd661))

* Merge pull request #35 from Jc2k/track_staleness

Automatic replacement of stale containers ([`25ad943`](https://github.com/Jc2k/pytest-docker-tools/commit/25ad9436ebfe6a21dc5e3346bcaf7d0f2e9dc92e))

* Lint ([`6b56bd9`](https://github.com/Jc2k/pytest-docker-tools/commit/6b56bd92a625f88fbd7b9210da687a4055e2e1ba))

* Add tests for image_or_build ([`8614aa1`](https://github.com/Jc2k/pytest-docker-tools/commit/8614aa1081f941dcdd21f7892285f3c7b7d0bd09))

* Switch to pytest.fail to be consistent ([`15a9ee6`](https://github.com/Jc2k/pytest-docker-tools/commit/15a9ee618b2b77859a626d6a60b0dc1fed359ebe))

* Update README to mention staleness tracking ([`0a98042`](https://github.com/Jc2k/pytest-docker-tools/commit/0a980421f2f3279c1fd057e9e0bb8be429e13848))

* Add unittests for network and volume helpers ([`2d951d6`](https://github.com/Jc2k/pytest-docker-tools/commit/2d951d6ef59c53b7e0eb3e22f6d0c30532894cb2))

* Integration tests for image() ([`b655b38`](https://github.com/Jc2k/pytest-docker-tools/commit/b655b383a327ed9309e187b2d813cf3180fc2b5b))

* Add unittests for signature handling ([`d87b8ad`](https://github.com/Jc2k/pytest-docker-tools/commit/d87b8ad125e9bee6e376323a1965216acef42fcb))

* Add test for conflicting container when removing stale network ([`e2999b0`](https://github.com/Jc2k/pytest-docker-tools/commit/e2999b0a79c95b9f1fcf709b43afb65b6ca3a0a4))

* Add test for conflicting container when removing stale volume ([`91c0797`](https://github.com/Jc2k/pytest-docker-tools/commit/91c0797845e472290ca49219ff0e9ace9a38a4a1))

* Lint ([`c8f324c`](https://github.com/Jc2k/pytest-docker-tools/commit/c8f324ccada3788d907d00d52b5dbb7ac1c9a2f7))

* More cleanup before merging ([`fe0996b`](https://github.com/Jc2k/pytest-docker-tools/commit/fe0996bdb2df44353bd13ff77ecdc9a15af09ba7))

* Some refactoring + test coverage for container factory ([`36190e7`](https://github.com/Jc2k/pytest-docker-tools/commit/36190e7980ae70bd7f176f0f9c1d9f6ea3206fc3))

* Test test_reusable_conflict for networks ([`572184b`](https://github.com/Jc2k/pytest-docker-tools/commit/572184bcbcc3bdeb98be8abfa808da05ef40d9e2))

* Check error message for test_reusable_conflict ([`b6b77a6`](https://github.com/Jc2k/pytest-docker-tools/commit/b6b77a6bdfa71721d8ebe951b6066ebe378d6497))

* It should be an error if you try to use a volume that pytest-docker-tools didn&#39;t create ([`0b34fa9`](https://github.com/Jc2k/pytest-docker-tools/commit/0b34fa9bd1a5ae664fb57c168ecd1fa77bc01e2a))

* Rebuild containers if underlying netowrks and volumes change ([`30fbea1`](https://github.com/Jc2k/pytest-docker-tools/commit/30fbea11093ce8cfb852072b4a622bb34a6c0ebd))

* Automatic replacement of stale volumes ([`1f9074d`](https://github.com/Jc2k/pytest-docker-tools/commit/1f9074db3fb6294d286e3c40a999f2fbfe616ed7))

* Automatic replacement of stale networks ([`4ee3d14`](https://github.com/Jc2k/pytest-docker-tools/commit/4ee3d14345c446bb2c7aa28804e9ed56f3997bb4))

* Automatic replacement of stale containers ([`b824455`](https://github.com/Jc2k/pytest-docker-tools/commit/b824455947eae050f17cf9774bf438cfe68d2883))

* Add missing file ([`2456175`](https://github.com/Jc2k/pytest-docker-tools/commit/24561753f4872ebb83eca1a511c6fda778e35c95))

* Allow tests themselves to run under pytest-xdist ([`0aae7ea`](https://github.com/Jc2k/pytest-docker-tools/commit/0aae7ea5d14e33f44063f47d64ada036341957e7))

* Test compatibility with pytest-xdist ([`25535f0`](https://github.com/Jc2k/pytest-docker-tools/commit/25535f0c9e07275c60208fe1c5f58e9826679b63))

* Update dev notes ([`dedbefd`](https://github.com/Jc2k/pytest-docker-tools/commit/dedbefd7598e7827fcfa9ef153e527563ebb9165))

* Version bump ([`cb8ee97`](https://github.com/Jc2k/pytest-docker-tools/commit/cb8ee97002ee502617fe1b3e050eaaebf0870764))

* Add support for tagging build stages ([`9b89624`](https://github.com/Jc2k/pytest-docker-tools/commit/9b896244fe847d11b989353d61407b3951de13eb))

* Make &#39;reusable-container&#39; label just &#39;reusable&#39; as applies to networks, volumes, etc ([`eef72b9`](https://github.com/Jc2k/pytest-docker-tools/commit/eef72b9ed56faedaac322287e3aae9b366642b77))

* Merge pull request #32 from alexanderpetrenz/tests_reusable ([`cf5df26`](https://github.com/Jc2k/pytest-docker-tools/commit/cf5df26aa6da5a70891ab797e44180bbfd137566))

* Merge pull request #30 from Jc2k/tests_reusable ([`de9a68c`](https://github.com/Jc2k/pytest-docker-tools/commit/de9a68c1c0b797e7f8b04ff5efdab633a76ddf49))

* adopted README.md ([`93ec324`](https://github.com/Jc2k/pytest-docker-tools/commit/93ec324243ee227c860ab480bfd13f800838b888))

* Test we can set own labels on container, volume and network ([`fd477d7`](https://github.com/Jc2k/pytest-docker-tools/commit/fd477d7ca026e4a1e7592ef9ae4bd86d87a1da12))

* Allow test authors to set their own labels ([`8c443a5`](https://github.com/Jc2k/pytest-docker-tools/commit/8c443a51daa6a9f63931c5c79ee089c51ee79591))

* Fix labels ([`371c8de`](https://github.com/Jc2k/pytest-docker-tools/commit/371c8de80c9ee87e422356227c4eb7e500a4a3aa))

* Assert fails if reuse without name ([`60a0f64`](https://github.com/Jc2k/pytest-docker-tools/commit/60a0f64fc6465834c49635a31095d9c4d0eb3ddd))

* Implement reuse for voumes and networks ([`473a71b`](https://github.com/Jc2k/pytest-docker-tools/commit/473a71b4c7b13f347b2bf9adb9d3a0a093947a2f))

* Assert containers are reused ([`5bddcdb`](https://github.com/Jc2k/pytest-docker-tools/commit/5bddcdb089e3f6d16a70d5a82f8e6a61c8c403a7))

* Version bump ([`662a4da`](https://github.com/Jc2k/pytest-docker-tools/commit/662a4da1d0d51ce2c6a3a5f93aab90166278c9ed))

* Merge branch &#39;main&#39; of github.com:Jc2k/pytest-docker-tools into main ([`7b3faf5`](https://github.com/Jc2k/pytest-docker-tools/commit/7b3faf54c7eda3b0d549ff8071af09f9b3d2ead3))

* Version bump ([`d99bdfb`](https://github.com/Jc2k/pytest-docker-tools/commit/d99bdfb430b83ddfd74a5d6649af938c13663dba))

* Merge pull request #29 from alexanderpetrenz/main

now evaluating --reuse-containers in network fixture factory ([`46f6ac1`](https://github.com/Jc2k/pytest-docker-tools/commit/46f6ac1f0ff88fedf418e5a40cf2d6785f027610))

* black ([`9e26e9e`](https://github.com/Jc2k/pytest-docker-tools/commit/9e26e9ef9801a1d8dbbe128cd582ed8785cc13d0))

* added volume test that covers reusable-container option ([`d7e580a`](https://github.com/Jc2k/pytest-docker-tools/commit/d7e580a1b897ec12f02b77225c79bd05e6b1c932))

* now handling --reused_containers in volume fixture ([`34e3efa`](https://github.com/Jc2k/pytest-docker-tools/commit/34e3efa133009972e6ce20b3e1f9a72b41a7a161))

* removed unused import ([`b27b31e`](https://github.com/Jc2k/pytest-docker-tools/commit/b27b31e2caf0842b5ebf45721cad07b6a7c6b260))

* black ([`3da37d1`](https://github.com/Jc2k/pytest-docker-tools/commit/3da37d1f2380adab21afaeb87a856de990010957))

* newline ([`fd1a513`](https://github.com/Jc2k/pytest-docker-tools/commit/fd1a5132214e9ffab431e644a6bec9cb43aa4ea7))

* newline ([`0f0baa2`](https://github.com/Jc2k/pytest-docker-tools/commit/0f0baa25d8e13be093f17ab7fa22bd1efc8591b8))

* black fix ([`38d357a`](https://github.com/Jc2k/pytest-docker-tools/commit/38d357acf7089f8e33baa9e7f40c0f8886cc9297))

* created second network test ([`92b6989`](https://github.com/Jc2k/pytest-docker-tools/commit/92b69896ed67632c6e4f4fac3b91ebff44c87639))

* now evaluating --reuse-containers in network fixture factory to avoid attempting to delete network with active containers ([`e813c38`](https://github.com/Jc2k/pytest-docker-tools/commit/e813c387df9d9ec72741155147a5fe1ccb3102e8))

* Version bump ([`b161a3a`](https://github.com/Jc2k/pytest-docker-tools/commit/b161a3aba2556f9485cca7fa8ca50cde65ca45cd))

* Update release script ([`94a4419`](https://github.com/Jc2k/pytest-docker-tools/commit/94a441914a4d2278f5df940fc4f04219957cbdf1))

* Dependency bumps ([`5f09a8b`](https://github.com/Jc2k/pytest-docker-tools/commit/5f09a8bdb5429886fe4d9e6bf8f4fad3b170c678))

* Merge pull request #27 from alexanderpetrenz/main

Introducing Reusable Containers ([`4bbc9ef`](https://github.com/Jc2k/pytest-docker-tools/commit/4bbc9ef712751b6fb2059829d8b6ae44cd323c36))

* adjustments on README.md ([`5c9bb1f`](https://github.com/Jc2k/pytest-docker-tools/commit/5c9bb1fe4bffe7191da9faca92f26ac5b632a1a9))

* adjustments on README.md ([`3aa511f`](https://github.com/Jc2k/pytest-docker-tools/commit/3aa511f91ca6b2b10c99385bbe96ac2004c0112f))

* black adjustment ([`f11705f`](https://github.com/Jc2k/pytest-docker-tools/commit/f11705f476c5736a02f2e943a8f6ccc94a3f7cad))

* renamed Label constant ([`cd3b403`](https://github.com/Jc2k/pytest-docker-tools/commit/cd3b403b8e55962df5862b2687e43fead43f32d1))

* simplified is_reusable_container() ([`43eb6d8`](https://github.com/Jc2k/pytest-docker-tools/commit/43eb6d84c57217847a85445fdb031fb7cedc7b67))

* black related adjustments ([`62e3654`](https://github.com/Jc2k/pytest-docker-tools/commit/62e365479fb76d55f20d340df54cfd17c3e9d950))

* isort related adjustments ([`cedee74`](https://github.com/Jc2k/pytest-docker-tools/commit/cedee744538bf22232e478bad069c3a6d1991c96))

* + lower case labels
+ command line argument renamed to --reuse-containers
+ defined constant for label &#39;pytest-docker-tools.reusable-container&#39;
+ replaced RuntimeException with pytest.UsageException
+ added helper method is_reusable_container ([`4a690a3`](https://github.com/Jc2k/pytest-docker-tools/commit/4a690a38f908451f52ae542922b919e460b2d53b))

* added empty line ([`6cb6884`](https://github.com/Jc2k/pytest-docker-tools/commit/6cb6884246edf1764431c893a1dfa6ec092be0fa))

* now testing image fixture_factory ([`8c26e00`](https://github.com/Jc2k/pytest-docker-tools/commit/8c26e0083200572d718f8dbd2dd83901a1e678ec))

* black related fixes ([`f8e1de7`](https://github.com/Jc2k/pytest-docker-tools/commit/f8e1de756c254472a3012636d42ae3215dc201dd))

* resetting build path in orchestration fix ([`cb5afc8`](https://github.com/Jc2k/pytest-docker-tools/commit/cb5afc8e96a6e76bb9e34cc8084683b46d887aa6))

* import order fix ([`05172a1`](https://github.com/Jc2k/pytest-docker-tools/commit/05172a1f472f5ea606e70d74cc713695d5e56ab5))

* minor fixes ([`a27ee9b`](https://github.com/Jc2k/pytest-docker-tools/commit/a27ee9b82117a3bc6e2a20331b8e5f35b29e197e))

* docu fix ([`57ebef5`](https://github.com/Jc2k/pytest-docker-tools/commit/57ebef52ae055407c9d0d5d79237689a56b58f01))

* adding documentation to README.md ([`07ba654`](https://github.com/Jc2k/pytest-docker-tools/commit/07ba654cdc96e4473cbede54aee1c645ae0b46ce))

* fixing orchestration test by providing absolute path ([`de49eb2`](https://github.com/Jc2k/pytest-docker-tools/commit/de49eb2bc017d1d61067ec863a919c4cb67b05ca))

* added test cases for container fixture factory ([`af2dbb4`](https://github.com/Jc2k/pytest-docker-tools/commit/af2dbb423db1987f8cefc1985539d19ee8ba0e03))

* added documentation ([`5c01e11`](https://github.com/Jc2k/pytest-docker-tools/commit/5c01e1137ba4ec91f2e8b63306d4b4c3fbc7e59e))

* Adding command line option &#39;--reuse_containers&#39;

This option needs a given &#39;name&#39; container attribute which is used to search for an already existing container.
If such a container exists it will be reused. If not a new container will be created.
The finalizer for removing the container at the end of test execution is not added if --reuse_containers is set ([`28d6d1d`](https://github.com/Jc2k/pytest-docker-tools/commit/28d6d1d8d52aea71ed3c1821d8f866d4fdb3f33d))

* Merge pull request #1 from Jc2k/main

update ([`cdb1478`](https://github.com/Jc2k/pytest-docker-tools/commit/cdb1478e80ee38a05791c22e65a0368e4f9143fe))

* Version bump ([`5866603`](https://github.com/Jc2k/pytest-docker-tools/commit/58666031755aea49b17f3b9a9af14653e3114c71))

* Run black ([`a7835b0`](https://github.com/Jc2k/pytest-docker-tools/commit/a7835b0de2a7aac1fec885ca300f056f58170c04))

* Merge pull request #26 from bertpassek/bugfix

bugfix: fixed TypeError: &#39;NoneType&#39; object is not subscriptable ([`ae2442a`](https://github.com/Jc2k/pytest-docker-tools/commit/ae2442a636ff72bf4fba025297900b453dda7512))

* bugfix: fixed TypeError: &#39;NoneType&#39; object is not subscriptable ([`db70d65`](https://github.com/Jc2k/pytest-docker-tools/commit/db70d65a20e5b14eb05089f3de04b4049f8754fc))

* Version bump ([`06ac93c`](https://github.com/Jc2k/pytest-docker-tools/commit/06ac93c212c43f6bd626d2be7ede462da90c8af7))

* Fix #24 ([`2dcb931`](https://github.com/Jc2k/pytest-docker-tools/commit/2dcb93152010530a9543be0feb8cc7470331da9b))

* Add example for #19 ([`4537ab1`](https://github.com/Jc2k/pytest-docker-tools/commit/4537ab1525641b0fd51d0eaf101435e8d9fefc64))

* Version bump ([`f873aae`](https://github.com/Jc2k/pytest-docker-tools/commit/f873aaed47effbc4ca0cd0a0edf3edcaac2cacee))

* Version bumps ([`d2c44ab`](https://github.com/Jc2k/pytest-docker-tools/commit/d2c44ab3dd335363f19ea49a3ab4f31dfb89fb97))

* Test against python 3.9 ([`ed88718`](https://github.com/Jc2k/pytest-docker-tools/commit/ed887181cfa311209159479f773ad0a5fb7b6fd3))

* Merge pull request #22 from alexanderpetrenz/main

Fixing/Replacing Function utils.tests_inside_container ([`0601194`](https://github.com/Jc2k/pytest-docker-tools/commit/060119491173efd78ff5c34230b329aec5a1fec7))

* Fix GitHub Actions config after they removed their set-env stuff ([`e004c42`](https://github.com/Jc2k/pytest-docker-tools/commit/e004c4237f9257b46e1580424ab4edbfb0bf92d2))

* replaced implementation of utils.tests_inside_container as discussed in https://github.com/Jc2k/pytest-docker-tools/issues/20 ([`97128b6`](https://github.com/Jc2k/pytest-docker-tools/commit/97128b6118c6242c42794769444c5d70fc95992f))

* Improve coverage reporting ([`d8b2efa`](https://github.com/Jc2k/pytest-docker-tools/commit/d8b2efa9cbf4d1f84c9a88cdd1f3a655896ffae4))

* Version bump ([`2811d80`](https://github.com/Jc2k/pytest-docker-tools/commit/2811d80a17c71f92f96d276d97762929c7911a16))

* Merge pull request #15 from Jc2k/modernize

Switch to GitHub actions and enable some of the usual linters ([`b030d51`](https://github.com/Jc2k/pytest-docker-tools/commit/b030d5170ed0e20f4ec43c14c1a43a9a9e7abd6c))

* Fix deprecation warnings ([`189f546`](https://github.com/Jc2k/pytest-docker-tools/commit/189f546bfb13fe7051b49feaa09fee5772564673))

* Install new pytest-markdown ([`179d83d`](https://github.com/Jc2k/pytest-docker-tools/commit/179d83dc1a3c3ac49ca8d3ff2cd7e45d8220023b))

* Remove travis.yml ([`5f84e9f`](https://github.com/Jc2k/pytest-docker-tools/commit/5f84e9f34f4b210c1d9f01acddb5e434be854fc3))

* Update test matrix ([`86f5dab`](https://github.com/Jc2k/pytest-docker-tools/commit/86f5daba628ef5392c8ea022976bf68504014afd))

* Add codecov to dev pkgs ([`05d6f21`](https://github.com/Jc2k/pytest-docker-tools/commit/05d6f21e68d5f00f7d0d0912759964592e436438))

* Remove .travis.yml ([`e5a340a`](https://github.com/Jc2k/pytest-docker-tools/commit/e5a340a5097d6e11cb5e394bee395e6e30c14550))

* Switch to GitHub actions and enable some of the usual linters ([`d45467b`](https://github.com/Jc2k/pytest-docker-tools/commit/d45467bff2e0e1a507940bdd549a3fbd9835b5cd))

* Release 0.2.3 ([`cc9a2ae`](https://github.com/Jc2k/pytest-docker-tools/commit/cc9a2ae1f804d3d69e1376a48fccb7b53d2d3951))

* Merge pull request #14 from alexpdp7/alexpdp7/stringiodockerfile

Support creating images from BytesIO Dockerfiles #13 ([`d230e4d`](https://github.com/Jc2k/pytest-docker-tools/commit/d230e4dce1c930a5215d0898b0065d0b9a6499b1))

* Document how to create a container using BytesIO as the Dockerfile

* Patch some cosmetic issues that arise doing so ([`97b8ee0`](https://github.com/Jc2k/pytest-docker-tools/commit/97b8ee0d8a99517e0d6173cbb647cd64cd760359))

* Update README.md with development instructions ([`65b068b`](https://github.com/Jc2k/pytest-docker-tools/commit/65b068bab531dbb6f0012caf523d1cbb7e11933b))

* Ignore coverage artifacts ([`013d2ff`](https://github.com/Jc2k/pytest-docker-tools/commit/013d2ffc012fb001ab56f2e4da2a1be716461565))

* Release 0.2.2 ([`4cfc68a`](https://github.com/Jc2k/pytest-docker-tools/commit/4cfc68ada31745605325bdd420ad10f3f995112d))

* Merge pull request #12 from soufyakoub/timeout_documentation

Update README.md ([`26e4602`](https://github.com/Jc2k/pytest-docker-tools/commit/26e4602d7f1b59fc03d063202e37e4b249c11f58))

* Add boilerplate for pytest-markdown tests ([`3ec2edb`](https://github.com/Jc2k/pytest-docker-tools/commit/3ec2edb4a7841b2e1f6d90682f058ae209738f84))

* Update README.md ([`71bc73e`](https://github.com/Jc2k/pytest-docker-tools/commit/71bc73e7b5db067f14dd233ebc65ff461e2f3132))

* Merge pull request #11 from soufyakoub/TypeError_fix

Closes #9: Fix container timeout TypeError ([`4baecbc`](https://github.com/Jc2k/pytest-docker-tools/commit/4baecbcf5092fd2132ad6a1ab785731ef0985a05))

* Closes #9: Fix container timeout TypeError ([`5cca04e`](https://github.com/Jc2k/pytest-docker-tools/commit/5cca04e50953811a4dc3458839cecf8376ee1b4a))

* 0.2.1 ([`1de7d05`](https://github.com/Jc2k/pytest-docker-tools/commit/1de7d05ec758696bd6af700a224b892bb8fbeab7))

* Merge pull request #10 from soufyakoub/wait_for_callable_timeout

Closes #9 : get timeout value from keyword arg ([`6ef282c`](https://github.com/Jc2k/pytest-docker-tools/commit/6ef282c4e37fe8e6da64c0a00846648c2aaa321b))

* Closes #9 : get timeout value from keyword arg ([`ed09d93`](https://github.com/Jc2k/pytest-docker-tools/commit/ed09d93b1c18ad9a6f388c929144b9da3bcc63ad))

* Merge pull request #7 from Jc2k/dependabot/pip/urllib3-1.24.2

Bump urllib3 from 1.23 to 1.24.2 ([`34a8851`](https://github.com/Jc2k/pytest-docker-tools/commit/34a8851a1aa8f8ca95f01193ab048dbc1e9e0eb9))

* Bump urllib3 from 1.23 to 1.24.2

Bumps [urllib3](https://github.com/urllib3/urllib3) from 1.23 to 1.24.2.
- [Release notes](https://github.com/urllib3/urllib3/releases)
- [Changelog](https://github.com/urllib3/urllib3/blob/master/CHANGES.rst)
- [Commits](https://github.com/urllib3/urllib3/compare/1.23...1.24.2)

Signed-off-by: dependabot[bot] &lt;support@github.com&gt; ([`25a1d7a`](https://github.com/Jc2k/pytest-docker-tools/commit/25a1d7afe4c6432d0aff9a63bfba845e57b1fa00))

* 0.2.0 ([`645ad55`](https://github.com/Jc2k/pytest-docker-tools/commit/645ad55d55d14cfead8f0d73823089c1de79c456))

* Merge remote-tracking branch &#39;origin/master&#39; ([`46ceb13`](https://github.com/Jc2k/pytest-docker-tools/commit/46ceb1300239ac079db0060ec2919cc47080220d))

* Merge pull request #3 from terrycain/master

Added IPv6 port binding support ([`6bfd8e4`](https://github.com/Jc2k/pytest-docker-tools/commit/6bfd8e44737771aaf0d2f4a86f4a269cb0f9808a))

* Add a test for #2 ([`f1b2297`](https://github.com/Jc2k/pytest-docker-tools/commit/f1b22978049d657d79b5d89d98b487f458010358))

* Bump requests version ([`8d06d52`](https://github.com/Jc2k/pytest-docker-tools/commit/8d06d52c9fcc08f46b6504237630b729c49a665f))

* Added IPv6 port binding support ([`ceb4e88`](https://github.com/Jc2k/pytest-docker-tools/commit/ceb4e886473cd4ffb23b9c7b3bbfe5aae6dae24b))

* 0.1.0 ([`0c561eb`](https://github.com/Jc2k/pytest-docker-tools/commit/0c561ebbeb5fd9e26975ab9fba286427bb103fdb))

* Don&#39;t look in kwargs for environ_key ([`824416e`](https://github.com/Jc2k/pytest-docker-tools/commit/824416e6889f18d334897c951b635a8510ee9308))

* 0.0.12 ([`cd476f2`](https://github.com/Jc2k/pytest-docker-tools/commit/cd476f2753b814c2c698bd609ca7ee073704b332))

* First split should be on new lines ([`d784fb6`](https://github.com/Jc2k/pytest-docker-tools/commit/d784fb6235c1bb2066d7cded74be49ccd95a5ba7))

* Add restart helper that waits for container to be ready again ([`b65d2d3`](https://github.com/Jc2k/pytest-docker-tools/commit/b65d2d3276cc3b70501389317983c15835a3bf06))

* Flake8 fixes ([`bb3525e`](https://github.com/Jc2k/pytest-docker-tools/commit/bb3525e61ed684e2ea80a222eb8f5f7d84bdd7fa))

* Add heper for getting address ([`9c83304`](https://github.com/Jc2k/pytest-docker-tools/commit/9c83304bd12d7d633de90ec49107702cf15f76a8))

* Add &#39;image_or_build&#39; factory ([`c47f3d1`](https://github.com/Jc2k/pytest-docker-tools/commit/c47f3d17bb94bb3ea956b55d370ce6b8f060b7c8))

* Add &#39;image&#39; factory ([`9ddd912`](https://github.com/Jc2k/pytest-docker-tools/commit/9ddd9121941d086f088b40db35d5e7a74e7b794f))

* 0.0.11 ([`d61cf4e`](https://github.com/Jc2k/pytest-docker-tools/commit/d61cf4e6a249a07bfa35dd5ef4142d1c088bd969))

* Missing file ([`dcfda5f`](https://github.com/Jc2k/pytest-docker-tools/commit/dcfda5f8adb72cae4428f36dcedf802d57ceeaac))

* Better log capture during fixture setup ([`e9c136d`](https://github.com/Jc2k/pytest-docker-tools/commit/e9c136d9f2cec8fd00e44bcd50f4631ec223330f))

* 0.0.10 ([`0e94139`](https://github.com/Jc2k/pytest-docker-tools/commit/0e941391e75430c8e9b670c10b167c1be69bf61b))

* Fix get_text ([`dca432b`](https://github.com/Jc2k/pytest-docker-tools/commit/dca432bf0e0140c6058baedbba0f38a6b49b707a))

* 0.0.9 ([`02cdb1d`](https://github.com/Jc2k/pytest-docker-tools/commit/02cdb1d569aac3383605433bc270228cdbc26d03))

* Fix get_text wrapper ([`84cab44`](https://github.com/Jc2k/pytest-docker-tools/commit/84cab444e6f41e754df614726949b049d6747550))

* Allow fixture factory users to supply a wrapper_class ([`c1c6ce2`](https://github.com/Jc2k/pytest-docker-tools/commit/c1c6ce2e060b24ec506d6df94c9f6715a5f87b8a))

* Towards #1 - show how fixture scope applies to docker fixtures ([`68076f7`](https://github.com/Jc2k/pytest-docker-tools/commit/68076f79ace7f8ec14f7dd51377c46859a01daa5))

* Fix compat with py.test 3.7.0 and release 0.0.8 ([`02dc3a2`](https://github.com/Jc2k/pytest-docker-tools/commit/02dc3a2679cb4d6853ce315e975e84877416eb2b))

* Version bump ([`f06ebe1`](https://github.com/Jc2k/pytest-docker-tools/commit/f06ebe1f2865e44158fde045cdb05bd2e226a040))

* Tidy up intermediate containers ([`f262a9b`](https://github.com/Jc2k/pytest-docker-tools/commit/f262a9be9fe5c9126cd232d034ef86a1a674bd78))

* Add Dockerfile needed by previous commit ([`8603305`](https://github.com/Jc2k/pytest-docker-tools/commit/860330577e1c9636aca7f34d2ba4ba677a9c2f03))

* Allow volumes to be seeded with initial content ([`40f2676`](https://github.com/Jc2k/pytest-docker-tools/commit/40f2676c37e0f815c5065e27e5a0848a3d1f7bc0))

* 0.0.6 ([`a52b727`](https://github.com/Jc2k/pytest-docker-tools/commit/a52b727cb2070a16af19e75fec54b894aa1bc2c4))

* Don&#39;t crash if fixture hasn&#39;t been evaluated yet ([`ea88d4d`](https://github.com/Jc2k/pytest-docker-tools/commit/ea88d4d26c83f54e729e0044e5900c1c042e3e15))

* Bump pytest-markdown for better section names ([`68b4868`](https://github.com/Jc2k/pytest-docker-tools/commit/68b4868103887a0aa8f69acbfa0a730498b364ab))

* 0.0.5 ([`610fdd5`](https://github.com/Jc2k/pytest-docker-tools/commit/610fdd5e393e3f5d69ef81835508c6f326d226dd))

* Image fetch terminology fix ([`45d3327`](https://github.com/Jc2k/pytest-docker-tools/commit/45d33272b9276fc1c69d31dc580ad464c533723c))

* Allow users of factories to customize more stuff ([`d41c024`](https://github.com/Jc2k/pytest-docker-tools/commit/d41c024c515b56664a2a81ad65431ae6f3af4769))

* Convert all factories to use the decorator ([`46e38d6`](https://github.com/Jc2k/pytest-docker-tools/commit/46e38d66bf7fcf3e8ae8265b4150dec75faa89f6))

* Pull all templating and factory-izing contain out so it can be shared ([`75485ab`](https://github.com/Jc2k/pytest-docker-tools/commit/75485abfbb01764a8a019cf4e8b6680949f9bd54))

* Pull template handling out of container specific code ([`4dd9b8b`](https://github.com/Jc2k/pytest-docker-tools/commit/4dd9b8b6fe462680534c8208510dae3710eecad5))

* Use awful code generation for fixture generation - this gives up proper static ahead of time dependencies ([`5bc9762`](https://github.com/Jc2k/pytest-docker-tools/commit/5bc976254e922587dc032fa5552239a5c961a65a))

* Add a visitor that can extract a list of fixtures used during test setup ([`a7435a6`](https://github.com/Jc2k/pytest-docker-tools/commit/a7435a6381868c574f47eac11880d614f294e1a3))

* Markdown tests are now a seperate plugin ([`e3add1f`](https://github.com/Jc2k/pytest-docker-tools/commit/e3add1fb1ff1dfcb3e8d83905337c99c9995bcc2))

* Bump to 0.0.4 ([`4c774e3`](https://github.com/Jc2k/pytest-docker-tools/commit/4c774e3e39da088a984b1565358a0c407243b19d))

* Example tests in README are now executed by pytest ([`dac1cbc`](https://github.com/Jc2k/pytest-docker-tools/commit/dac1cbcf1dcc745a0afa79e03637a63ab90969bc))

* Towards README testing ([`7a5874a`](https://github.com/Jc2k/pytest-docker-tools/commit/7a5874a350c28321e6817e80fe60d8feda5952fa))

* Show how you can make client fixtures that build on the apiserver server fixture ([`492b163`](https://github.com/Jc2k/pytest-docker-tools/commit/492b1634403202c8ceccb050e716780874f04215))

* Any code blocks marked &#39;# conftest.py&#39; will contribute fixtures towards other tests in the same header block ([`54679c6`](https://github.com/Jc2k/pytest-docker-tools/commit/54679c6d15a7d44e762e92be4e2c2b3c2d9f480f))

* Ignore __pycache__ files ([`938b99c`](https://github.com/Jc2k/pytest-docker-tools/commit/938b99c97cc24d635bde3bc1487fbf69e662d313))

* Add an example &#39;microservice&#39; ([`6261968`](https://github.com/Jc2k/pytest-docker-tools/commit/6261968b98450084509bf8e026e498311402aa0f))

* Grim way of attaching logs of all relevant containers ([`a4d4024`](https://github.com/Jc2k/pytest-docker-tools/commit/a4d4024c0cbde4005cfc8a5c44be9b5b801e8d12))

* Group tests based on parent heading ([`bd9d067`](https://github.com/Jc2k/pytest-docker-tools/commit/bd9d067daaa83800bbbdd7dcd0373d34132e249c))

* Closer ([`7cf6b62`](https://github.com/Jc2k/pytest-docker-tools/commit/7cf6b625fdb6e1d18959b4a7ec6e7d61759239b1))

* Towards README tests ([`f09143c`](https://github.com/Jc2k/pytest-docker-tools/commit/f09143c16ac61f14c9b134918d3a08b123f8eb7f))

* Be explicit about imports in README ([`ae6a9d3`](https://github.com/Jc2k/pytest-docker-tools/commit/ae6a9d3ea96e516b55359811b71dacda7fffd902))

* Update README with syntax highlighting ([`f94a883`](https://github.com/Jc2k/pytest-docker-tools/commit/f94a883e78d5a98c6c81ae708e3feb5f15ac6363))

* Fix flake8 ([`b9a8356`](https://github.com/Jc2k/pytest-docker-tools/commit/b9a8356d951b8e7ba218dff9c0017de15f9629eb))

* Capture more logs more of the time ([`89b3dd8`](https://github.com/Jc2k/pytest-docker-tools/commit/89b3dd8f653b6907260fc4540db052a9da990799))

* Fix error when container has exited before starting ([`2fa3e33`](https://github.com/Jc2k/pytest-docker-tools/commit/2fa3e33200152d9b9ee56ce504e61a4bb9091218))

* Doc fixes ([`e0ef0d7`](https://github.com/Jc2k/pytest-docker-tools/commit/e0ef0d72471ab90a1aaf633eaa6b525975e62523))

* Pull in docker dep ([`31c24a3`](https://github.com/Jc2k/pytest-docker-tools/commit/31c24a3353fac31a4037d24d0d10e0568c7743a2))

* Version bump ([`a9901ea`](https://github.com/Jc2k/pytest-docker-tools/commit/a9901ead2374cab273eb034fc76867e172269435))

* Tighten docs ([`0109fdc`](https://github.com/Jc2k/pytest-docker-tools/commit/0109fdce80e20c0751a3ae62de0a7f84b84fde01))

* Document some of the more amazing pieces of gymnastics you can do with py.test fixtures ([`8b77faf`](https://github.com/Jc2k/pytest-docker-tools/commit/8b77fafe908fb26e4ad0d997c4f1970ba79e2303))

* Fix isort ([`1d4e8e5`](https://github.com/Jc2k/pytest-docker-tools/commit/1d4e8e5288d99c9fc9b28ae5e8014be2022cbf26))

* Document docker_client ([`332757a`](https://github.com/Jc2k/pytest-docker-tools/commit/332757a45898f954cf3218e3b84fbd420361cf36))

* Document how to get logs from container ([`2bf27c9`](https://github.com/Jc2k/pytest-docker-tools/commit/2bf27c9ee05905b8f50efb692ce5798c8035914f))

* Review tests for xdist correctness ([`4f41622`](https://github.com/Jc2k/pytest-docker-tools/commit/4f41622e24821b30f556cecf1b899143f6f14e89))

* More docs ([`781d098`](https://github.com/Jc2k/pytest-docker-tools/commit/781d09840a774f8451921da5ac431a099bf7ae04))

* Running tests under xdist works ([`62d90f4`](https://github.com/Jc2k/pytest-docker-tools/commit/62d90f482d4c3a6c565b326780f7e015dcaa8d60))

* Make test less racey ([`9124504`](https://github.com/Jc2k/pytest-docker-tools/commit/9124504f8c9cb6d579878c28face9ec990bb660e))

* More docs ([`d428217`](https://github.com/Jc2k/pytest-docker-tools/commit/d428217ce1305d21f8e8c962159adbf144ec6353))

* More documentation ([`dcf03a6`](https://github.com/Jc2k/pytest-docker-tools/commit/dcf03a658bc429afa51a1d9ba9abf34a5a52c337))

* Install test deps on travis ([`65f3bc8`](https://github.com/Jc2k/pytest-docker-tools/commit/65f3bc8a93a63dffbe88194a7891b63d23092e23))

* Better API and docs ([`ae7cf2c`](https://github.com/Jc2k/pytest-docker-tools/commit/ae7cf2c4be7deb9c6ff342420cda3c79984404d8))

* Remove settings that don&#39;t apply any more ([`14a199d`](https://github.com/Jc2k/pytest-docker-tools/commit/14a199d990e9e6275ce9f34f28c7106e6b24c005))

* Update Trove classifiers ([`3f77a4a`](https://github.com/Jc2k/pytest-docker-tools/commit/3f77a4a5d921cf722e8ddbd8cca022f8266c2ec1))

* Install with flit ([`74ec981`](https://github.com/Jc2k/pytest-docker-tools/commit/74ec981e137d6b2067fd094a11c407847ac0dd72))

* Remove setup.py ([`b64fceb`](https://github.com/Jc2k/pytest-docker-tools/commit/b64fcebbf8483fedc00366d6840fc405a19f1773))

* flit: Add entrypoints ([`f0b8309`](https://github.com/Jc2k/pytest-docker-tools/commit/f0b830960e47c89d27f7b24383851c5319baa846))

* Add pyproject.toml ([`29ec9b6`](https://github.com/Jc2k/pytest-docker-tools/commit/29ec9b6e19115c221187a39f98148e785775cff0))

* Recurisvely allow referencing other fixtures from string templates ([`d549381`](https://github.com/Jc2k/pytest-docker-tools/commit/d5493817511c88f6ad6df5b831014d173d768bdf))

* Add a description ([`bd9790b`](https://github.com/Jc2k/pytest-docker-tools/commit/bd9790b920da0643caddb322c54c65490c748d7d))

* Back to development: 0.0.2 ([`b36de61`](https://github.com/Jc2k/pytest-docker-tools/commit/b36de61bc5e2b8faae8586ad52c3ef9327be6fba))

* Add MANIFEST.in ([`7a62b10`](https://github.com/Jc2k/pytest-docker-tools/commit/7a62b10660d21566efe58cce0b7d6d4ae7b7995f))

* Fix port/proto split ([`af95f01`](https://github.com/Jc2k/pytest-docker-tools/commit/af95f013832d7a8005f08995652ce5e31a2824c8))

* Avoid pytest-cov ([`7c4f0cd`](https://github.com/Jc2k/pytest-docker-tools/commit/7c4f0cdaa2df0fc7d318139a43602467a0e23fa5))

* Add missing module ([`1d65759`](https://github.com/Jc2k/pytest-docker-tools/commit/1d65759a568b867c972c06e3de77f8ca91675d1b))

* Return a container object from the container fixture instead of a dict ([`d877926`](https://github.com/Jc2k/pytest-docker-tools/commit/d877926c3f695bb79d370ab3732c393c7b31dcc5))

* Automatically wait for port to be ready if user exposes a port ([`89dcef4`](https://github.com/Jc2k/pytest-docker-tools/commit/89dcef48b072c9dad732d2556c45d9ed94aefa9d))

* Add a repository_image fixture that pulls the image ([`49fbc0f`](https://github.com/Jc2k/pytest-docker-tools/commit/49fbc0f7e08b849b97547027c6cbae861ca7cc98))

* Enable Docker in travis tests ([`c78cc7c`](https://github.com/Jc2k/pytest-docker-tools/commit/c78cc7c74b1178033ec1249a8e036ff97378fa09))

* Fix py.test paths in .travis.yml ([`ff93905`](https://github.com/Jc2k/pytest-docker-tools/commit/ff939053a2c1bf3c44e3da669bf6a5ff5665ebe0))

* Turn on Travis and add code coverage ([`b173ee4`](https://github.com/Jc2k/pytest-docker-tools/commit/b173ee45aa03f4d6d50013a6cfb993432ad53477))

* Support extracting IP when using custom networks ([`6e1e111`](https://github.com/Jc2k/pytest-docker-tools/commit/6e1e11155203d3f89a85ecbe50741467f6bbc028))

* Attach container to its own private fixturized network ([`c98c023`](https://github.com/Jc2k/pytest-docker-tools/commit/c98c0236a51398f313b69671512739b487de5e37))

* Can create test networks ([`63502ac`](https://github.com/Jc2k/pytest-docker-tools/commit/63502acc686ff587bbc48a28af1d14f908b27866))

* More complicated example ([`b6bb440`](https://github.com/Jc2k/pytest-docker-tools/commit/b6bb440730b3c5edb8d84f6acfde5bcd12979342))

* Update README to match API ([`f39e419`](https://github.com/Jc2k/pytest-docker-tools/commit/f39e419f633ea31f49532cae9c1048d2269883b9))

* More integration tests ([`cab3033`](https://github.com/Jc2k/pytest-docker-tools/commit/cab30334cd4aeba05f14567ee7c436e2be315d77))

* More integration tests ([`c703cd6`](https://github.com/Jc2k/pytest-docker-tools/commit/c703cd6546d025a092134e0d18794a4287016dc5))

* Flake8 fixes ([`4226397`](https://github.com/Jc2k/pytest-docker-tools/commit/4226397be39552e7bf1f9d9f6b75da23c52a4a4b))

* Flake8 and isort config ([`2c23213`](https://github.com/Jc2k/pytest-docker-tools/commit/2c232135687066458ecef2f6917c37182ff71b03))

* Actually test that a container is started ([`5bca459`](https://github.com/Jc2k/pytest-docker-tools/commit/5bca459f7d5a66e7f48981c808d228e2854b8003))

* First pass of extracting useful Docker integration testing fixtures ([`a2895b7`](https://github.com/Jc2k/pytest-docker-tools/commit/a2895b73e363b9c092d0f7f09fc1861d2c456cc6))

// A pretend network for the screenshot tests.
//
// Every HttpClient the app (or package:http, or Image.network) creates while a
// test runs is this one. Nothing ever leaves the machine: a request is answered
// from [FakeBackend.handler], sample pictures are served from test/appshots/
// media, and anything unknown gets a 404. Every request is recorded in
// [FakeBackend.requests] so a test can print what a screen asked for.
import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'dart:typed_data';

class FakeReply {
  FakeReply(this.status, this.body, {this.contentType = 'application/json'});

  FakeReply.json(Object? data, {int status = 200})
    : this(status, utf8.encode(jsonEncode(data)));

  /// The `{code, msg, data}` envelope the Cheeko Java backend answers with.
  FakeReply.envelope(Object? data)
    : this.json(<String, Object?>{'code': 0, 'msg': 'success', 'data': data});

  final int status;
  final List<int> body;
  final String contentType;
}

typedef FakeHandler = FakeReply? Function(String method, Uri uri, String body);

class FakeBackend {
  FakeBackend({required this.mediaDir});

  /// Folder the sample pictures are read from. A request whose last path
  /// segment names a file in here is answered with that file.
  final String mediaDir;

  /// Answers API calls. Returning null falls through to the media folder and
  /// then to a 404.
  FakeHandler? handler;

  final List<String> requests = <String>[];

  /// Holds a reply back until the returned future completes, so a test can
  /// photograph the "in flight" state. Null lets every reply through at once.
  Future<void>? Function(String method, Uri uri)? gate;

  FakeReply reply(String method, Uri uri, String body) {
    requests.add('$method $uri');
    final answer = handler?.call(method, uri, body);
    if (answer != null) return answer;

    final name = uri.pathSegments.isEmpty ? '' : uri.pathSegments.last;
    final file = File('$mediaDir/$name');
    if (name.isNotEmpty && file.existsSync()) {
      final lower = name.toLowerCase();
      return FakeReply(
        200,
        file.readAsBytesSync(),
        contentType: lower.endsWith('.png') ? 'image/png' : 'image/jpeg',
      );
    }
    return FakeReply.json(<String, Object?>{
      'code': 404,
      'msg': 'not found (fake)',
    }, status: 404);
  }
}

class FakeHttpOverrides extends HttpOverrides {
  FakeHttpOverrides(this.backend);

  final FakeBackend backend;

  @override
  HttpClient createHttpClient(SecurityContext? context) =>
      _FakeHttpClient(backend);
}

class _FakeHttpClient implements HttpClient {
  _FakeHttpClient(this.backend);

  final FakeBackend backend;

  @override
  bool autoUncompress = true;

  @override
  Duration? connectionTimeout;

  @override
  Duration idleTimeout = const Duration(seconds: 15);

  @override
  int? maxConnectionsPerHost;

  @override
  String? userAgent;

  @override
  Future<HttpClientRequest> openUrl(String method, Uri url) async =>
      _FakeRequest(backend, method, url);

  @override
  Future<HttpClientRequest> open(
    String method,
    String host,
    int port,
    String path,
  ) => openUrl(method, Uri(scheme: 'https', host: host, port: port, path: path));

  @override
  Future<HttpClientRequest> getUrl(Uri url) => openUrl('GET', url);
  @override
  Future<HttpClientRequest> postUrl(Uri url) => openUrl('POST', url);
  @override
  Future<HttpClientRequest> putUrl(Uri url) => openUrl('PUT', url);
  @override
  Future<HttpClientRequest> patchUrl(Uri url) => openUrl('PATCH', url);
  @override
  Future<HttpClientRequest> deleteUrl(Uri url) => openUrl('DELETE', url);
  @override
  Future<HttpClientRequest> headUrl(Uri url) => openUrl('HEAD', url);

  @override
  void close({bool force = false}) {}

  @override
  dynamic noSuchMethod(Invocation invocation) => null;
}

class _FakeHeaders implements HttpHeaders {
  final Map<String, List<String>> _values = <String, List<String>>{};

  @override
  List<String>? operator [](String name) => _values[name.toLowerCase()];

  @override
  void add(String name, Object value, {bool preserveHeaderCase = false}) {
    _values.putIfAbsent(name.toLowerCase(), () => <String>[]).add('$value');
  }

  @override
  void set(String name, Object value, {bool preserveHeaderCase = false}) {
    _values[name.toLowerCase()] = <String>['$value'];
  }

  @override
  String? value(String name) => _values[name.toLowerCase()]?.join(',');

  @override
  void remove(String name, Object value) =>
      _values[name.toLowerCase()]?.remove('$value');

  @override
  void removeAll(String name) => _values.remove(name.toLowerCase());

  @override
  void forEach(void Function(String name, List<String> values) action) =>
      _values.forEach(action);

  @override
  void clear() => _values.clear();

  @override
  ContentType? contentType;

  @override
  int contentLength = -1;

  @override
  bool chunkedTransferEncoding = false;

  @override
  bool persistentConnection = true;

  @override
  dynamic noSuchMethod(Invocation invocation) => null;
}

class _FakeRequest implements HttpClientRequest {
  _FakeRequest(this.backend, this.method, this.uri);

  final FakeBackend backend;

  @override
  final String method;

  @override
  final Uri uri;

  final BytesBuilder _body = BytesBuilder();
  final Completer<HttpClientResponse> _done = Completer<HttpClientResponse>();

  @override
  final HttpHeaders headers = _FakeHeaders();

  @override
  bool followRedirects = true;

  @override
  int maxRedirects = 5;

  @override
  int contentLength = -1;

  @override
  bool persistentConnection = true;

  @override
  bool bufferOutput = true;

  @override
  Encoding encoding = utf8;

  @override
  void add(List<int> data) => _body.add(data);

  @override
  void write(Object? object) => _body.add(utf8.encode('$object'));

  @override
  Future<void> addStream(Stream<List<int>> stream) async {
    await for (final chunk in stream) {
      _body.add(chunk);
    }
  }

  bool _closed = false;

  @override
  Future<HttpClientResponse> close() async {
    if (!_closed) {
      _closed = true;
      final hold = backend.gate?.call(method, uri);
      if (hold != null) await hold;
      final answer = backend.reply(
        method,
        uri,
        utf8.decode(_body.toBytes(), allowMalformed: true),
      );
      _done.complete(_FakeResponse(answer));
    }
    return _done.future;
  }

  @override
  Future<HttpClientResponse> get done => _done.future;

  @override
  Future<void> flush() async {}

  @override
  void abort([Object? exception, StackTrace? stackTrace]) {}

  @override
  dynamic noSuchMethod(Invocation invocation) => null;
}

class _FakeResponse extends Stream<List<int>> implements HttpClientResponse {
  _FakeResponse(this.reply) {
    headers.set('content-type', reply.contentType);
    headers.contentLength = reply.body.length;
  }

  final FakeReply reply;

  @override
  final HttpHeaders headers = _FakeHeaders();

  @override
  int get statusCode => reply.status;

  @override
  String get reasonPhrase => reply.status == 200 ? 'OK' : 'Not Found';

  @override
  int get contentLength => reply.body.length;

  @override
  HttpClientResponseCompressionState get compressionState =>
      HttpClientResponseCompressionState.notCompressed;

  @override
  bool get isRedirect => false;

  @override
  bool get persistentConnection => false;

  @override
  List<RedirectInfo> get redirects => const <RedirectInfo>[];

  @override
  List<Cookie> get cookies => const <Cookie>[];

  @override
  StreamSubscription<List<int>> listen(
    void Function(List<int> event)? onData, {
    Function? onError,
    void Function()? onDone,
    bool? cancelOnError,
  }) {
    return Stream<List<int>>.value(
      Uint8List.fromList(reply.body),
    ).listen(
      onData,
      onError: onError,
      onDone: onDone,
      cancelOnError: cancelOnError,
    );
  }

  @override
  dynamic noSuchMethod(Invocation invocation) => null;
}
